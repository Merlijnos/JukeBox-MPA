from django.db import models
import datetime

class Genre(models.Model):
    name = models.CharField(max_length=100)

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, default=1)
    duration = models.DurationField(default=datetime.timedelta(minutes=0))

class Playlist(models.Model):
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(Song)