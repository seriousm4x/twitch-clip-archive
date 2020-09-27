from django.db import models

# Create your models here.


class Clip(models.Model):
    clip_id = models.SlugField(max_length=100)
    url = models.URLField(max_length=150)
    embed_url = models.URLField(max_length=150)
    broadcaster_id = models.PositiveIntegerField()
    broadcaster_name = models.SlugField(max_length=30)
    creator_id = models.PositiveIntegerField()
    creator_name = models.SlugField(max_length=30)
    game_id = models.PositiveIntegerField(blank=True, null=True)
    language = models.CharField(max_length=6)
    title = models.CharField(max_length=150)
    view_count = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    thumbnail_url = models.URLField(max_length=150)
    clip_archived = models.BooleanField(default=False)
    thumbnail_archived = models.BooleanField(default=False)
    deleted_on_twitch = models.BooleanField(default=False)


class Game(models.Model):
    box_art_url = models.URLField(max_length=150, default="0")
    game_id = models.PositiveIntegerField(blank=True, null=True)
    name = models.CharField(max_length=150)


class TwitchSettings(models.Model):
    broadcaster_name = models.SlugField(
        max_length=30, null=False, default="CHANGE THIS")
    broadcaster_id = models.PositiveIntegerField(blank=True, null=True)
    client_id = models.SlugField(
        max_length=50, null=False, default="CHANGE THIS")
    client_secret = models.SlugField(
        max_length=50, null=False, default="CHANGE THIS")
    bearer = models.SlugField(max_length=50, blank=True, null=True)
