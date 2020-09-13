import datetime

import requests
from django.core.management.base import BaseCommand

from clips.models import Clip, Game, TwitchSettings


class Command(BaseCommand):
    def __init__(self):
        self.broadcaster_name = TwitchSettings.objects.get().broadcaster_name
        self.client_id = TwitchSettings.objects.get().client_id
        self.client_secret = TwitchSettings.objects.get().client_secret

        # refresh twitch credentials
        self.tokenurl = "https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials".format(
            self.client_id, self.client_secret)
        self.profileurl = "https://api.twitch.tv/helix/users?login={}".format(
            self.broadcaster_name)
        try:
            # get bearer token
            self.token_response = requests.post(self.tokenurl)
            self.token_response.raise_for_status()
            self.token_jsonResponse = self.token_response.json()
            self.bearer = self.token_jsonResponse["access_token"]

            self.helix_header = {
                "Client-ID": self.client_id,
                "Authorization": "Bearer {}".format(self.bearer),
            }

            self.kraken_header = {
                "Client-ID": self.client_id,
                "Authorization": "Bearer {}".format(self.bearer),
                "Accept": "application/vnd.twitchtv.v5+json"
            }

            # get broadcaster_id
            self.profile_response = requests.get(
                self.profileurl, headers=self.helix_header)
            self.profile_response.raise_for_status()
            self.profile_jsonResponse = self.profile_response.json()
            self.broadcaster_id = self.profile_jsonResponse["data"][0]["id"]

            # write to database
            TwitchSettings.objects.update_or_create(
                broadcaster_name=self.broadcaster_name,
                defaults={
                    "bearer": self.bearer,
                    "broadcaster_id": self.broadcaster_id
                }
            )

        except requests.exceptions.HTTPError as http_err:
            print("HTTP error occurred: {}".format(http_err))
        except Exception as err:
            print("Other error occurred: {}".format(err))

    def handle(self, **options):
        print("Updated Twitch credentials")
        print("Filling database with clips")
        self.updateClips()
        print("Success")
        print("Filling database with games")
        self.updateGames()
        print("Success")

    def updateClips(self):
        channel_creation_date = requests.get(
            "https://api.twitch.tv/kraken/channels/{}".format(
                self.broadcaster_id), headers=self.kraken_header).json()["created_at"]

        week = 1
        started_at = (datetime.datetime.now() -
                      datetime.timedelta(weeks=week)).isoformat("T")+"Z"
        api_url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&first=100&started_at={}".format(
            self.broadcaster_id, started_at)

        # add clips to db
        while True:
            req = requests.get(api_url, headers=self.helix_header)
            clips = req.json()

            for i in clips["data"]:
                valid_dict = i.copy()

                pop_keys = []
                for key, value in valid_dict.items():
                    if key not in [field.name for field in Clip._meta.get_fields()]:
                        pop_keys.append(key)
                    if value == "":
                        pop_keys.append(key)
                if pop_keys:
                    for key in pop_keys:
                        valid_dict.pop(key, None)

                clip_id = valid_dict["id"]
                valid_dict.pop("id", None)

                Clip.objects.update_or_create(
                    clip_id=clip_id,
                    defaults=valid_dict
                )

                # add game to db
                if "game_id" in valid_dict:
                    game_in_db = Game.objects.filter(
                        game_id=valid_dict["game_id"]).exists()
                    if not game_in_db:
                        game_req = requests.get(
                            "https://api.twitch.tv/helix/games?id={}".format(valid_dict["game_id"]), headers=self.helix_header)
                        game_title = game_req.json()["data"][0]["name"]
                        game_box_art_url = game_req.json()["data"][0]["box_art_url"].replace(
                            r"{width}x{height}", "70x93")
                        Game.objects.update_or_create(
                            game_id=valid_dict["game_id"],
                            defaults={
                                "name": game_title,
                                "box_art_url": game_box_art_url
                            }
                        )

            try:
                cursor = clips["pagination"]["cursor"]
                api_url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&first=100&started_at={}&after={}".format(
                    self.broadcaster_id, (datetime.datetime.now() - datetime.timedelta(weeks=week)).isoformat("T")+"Z", cursor)
            except KeyError:
                week += 1
                cursor_week = (datetime.datetime.now() -
                               datetime.timedelta(weeks=week)).isoformat("T")+"Z"
                if cursor_week < channel_creation_date:
                    print("Channel creation date reached")
                    break

                print(cursor_week)
                api_url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&first=100&started_at={}".format(
                    self.broadcaster_id, cursor_week)

    def updateGames(self):
        for game in Game.objects.all():
            game_req = requests.get(
                "https://api.twitch.tv/helix/games?id={}".format(game.game_id), headers=self.helix_header)
            try:
                game_title = game_req.json()["data"][0]["name"]
                game_box_art_url = game_req.json()["data"][0]["box_art_url"].replace(
                    r"{width}x{height}", "70x93")
                Game.objects.update_or_create(
                    game_id=game.game_id,
                    defaults={
                        "name": game_title,
                        "box_art_url": game_box_art_url
                    }
                )
            except IndexError:
                print(game.name, "got deleted on Twitch")
