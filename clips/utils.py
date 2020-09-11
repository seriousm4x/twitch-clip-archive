# these are custom functions to keep the views.py cleaner

from .models import Game
import clips


def matchGameToClip(cliplist):
    if type(cliplist) is clips.models.Clip:
        cliplist.game_title = Game.objects.filter(
            game_id=cliplist.game_id).get().name
        cliplist.game_thumbnail = Game.objects.filter(
            game_id=cliplist.game_id).get().box_art_url
    else:
        for clip in cliplist:
            clip.game_title = Game.objects.filter(
                game_id=clip.game_id).get().name
            clip.game_thumbnail = Game.objects.filter(
                game_id=clip.game_id).get().box_art_url
