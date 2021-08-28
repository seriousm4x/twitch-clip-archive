# these are custom functions to keep the views.py cleaner

from .models import Game
import clips


def matchGameToClip(cliplist):
    if type(cliplist) is clips.models.Clip:
        if cliplist.game_id == None:
            cliplist.game_title = "Unknown category"
        else:
            cliplist.game_title = Game.objects.filter(
                game_id=cliplist.game_id).get().name
            cliplist.game_thumb = Game.objects.filter(
                game_id=cliplist.game_id).get().box_art_url
    else:
        for clip in cliplist:
            if clip.game_id == None:
                clip.game_title = "Unknown category"
            else:
                clip.game_title = Game.objects.filter(
                    game_id=clip.game_id).get().name
                clip.game_thumb = Game.objects.filter(
                game_id=clip.game_id).get().box_art_url
