from django.db import models
from django.contrib.auth.models import User


class Mpapp_song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    spotify_id = models.CharField(max_length=200, default='default_value')


class CustomPlaylist(models.Model):
    objects = None
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField('Mpapp_song')

    class Meta:
        db_table = 'Mpapp_customplaylist'
        verbose_name = 'Custom Playlist'

    def __str__(self):
        return self.name
