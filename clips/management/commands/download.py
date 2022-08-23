import os
import shutil
from pathlib import Path

import requests
import yt_dlp
from django.conf import settings
from django.core.management.base import BaseCommand

from clips.models import Clip, Game


class Logger(object):
    def debug(self, msg):
        if "[download]" in msg:
            print(msg, end="", flush=True)
        else:
            print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

    def hook(self, d):
        if d["status"] == "finished":
            print("Done downloading, now converting ...")


class Command(BaseCommand):
    def __init__(self):
        self.all_clips = Clip.objects.all()

        # set download path for clips and thumbnails
        self.download_path = Path(settings.MEDIA_ROOT)
        self.clips_path = os.path.join(self.download_path, "clips")
        self.clip_thumbnails_path = os.path.join(
            self.download_path, "clip_thumbnails")
        self.game_thumbnails_path = os.path.join(
            self.download_path, "game_thumbnails")
        for path in self.download_path, self.clips_path, self.clip_thumbnails_path, self.game_thumbnails_path:
            if not os.path.exists(path):
                os.mkdir(path)

    def handle(self, **options):
        print("Downloading clips")
        self.downloadClips()
        print("Downloading clip thumbnails")
        self.downloadClipThumbs()
        print("Downloading game thumbnails")
        self.downloadGameThumbs()

    def downloadClips(self):
        i = 0
        for clip in self.all_clips:
            i += 1

            # skip clip if already archived
            if clip.clip_archived:
                print("Clip", i, "of", Clip.objects.count(),
                      "already archived", f"[{clip.clip_id}]")
                continue

            # skip clip deleted on twitch
            if clip.deleted_on_twitch:
                print("Clip", i, "of", Clip.objects.count(),
                      "deleted on twitch", f"[{clip.clip_id}]")
                continue

            ydl_opts = {
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "outtmpl": os.path.join(self.clips_path, clip.clip_id + ".mp4"),
                "logger": Logger(),
                "progress_hooks": [Logger().hook],
            }

            # download clip
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([clip.url])
                clip.clip_archived = True
                clip.deleted_on_twitch = False
                clip.save()
            except yt_dlp.utils.DownloadError:
                clip.deleted_on_twitch = True
                clip.save()

    def downloadClipThumbs(self):
        i = 0
        for clip in self.all_clips:
            i += 1
            print("Clip thumbnail", i, "of", Clip.objects.count(), clip.clip_id)

            # skip clip if already archived
            if clip.thumbnail_archived:
                print("Clip thumbnail already archived")
                continue

            # skip clip deleted on twitch
            if clip.deleted_on_twitch:
                print("Clip deleted on twitch")
                continue

            try:
                response = requests.get(clip.thumbnail_url, stream=True)
                with open(os.path.join(self.clip_thumbnails_path, clip.clip_id + ".jpg"), "wb") as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
                clip.thumbnail_archived = True
                clip.save()
            except requests.HTTPError as err:
                print(err)
                clip.deleted_on_twitch = True
                clip.save()

    def downloadGameThumbs(self):
        i = 0
        # we just download all game thumbs every time. maybe they change.
        for game in Game.objects.all():
            i += 1
            print("Game thumbnail", i, "of", Game.objects.count(), game.name)

            try:
                response = requests.get(game.box_art_url, stream=True)
                with open(os.path.join(self.game_thumbnails_path, str(game.game_id) + ".jpg"), "wb") as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
            except requests.HTTPError as err:
                print(err)
