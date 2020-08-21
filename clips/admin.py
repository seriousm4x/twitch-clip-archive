from django.contrib import admin

# Register your models here.
from .models import Clip, Game, TwitchSettings


class ClipAdmin(admin.ModelAdmin):
    list_display = ["title", "view_count", "creator_name", "created_at", "url"]
    search_fields = ["title", "creator_name", "clip_id"]
    list_filter = ["clip_archived", "thumbnail_archived", "deleted_on_twitch"]


class GameAdmin(admin.ModelAdmin):
    list_display = ["name", "game_id", "box_art_url"]
    search_fields = ["name"]


class TwitchSettingsAdmin(admin.ModelAdmin):
    list_display = ["broadcaster_name", "broadcaster_id",
                    "client_id", "client_secret", "bearer"]


admin.site.register(Clip, ClipAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(TwitchSettings, TwitchSettingsAdmin)
