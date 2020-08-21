# these are custom functions to keep the views.py cleaner

from .models import Game

def matchGameToClip(cliplist):
    for clip in cliplist:
        clip.game_title = Game.objects.filter(game_id=clip.game_id).get().name
        clip.game_thumbnail = Game.objects.filter(
            game_id=clip.game_id).get().box_art_url
