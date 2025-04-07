from django.db import models

class Song(models.Model):
    # songID = models.AutoField(primary_key=True)
    artist = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    spotifyURI = models.CharField(max_length=200)
    tags = models.CharField(max_length=200) # foreign key to tags

class Playlist(models.Model):
    playlistID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    spotifyID = models.CharField(max_length=200)
    generatedBy = models.IntegerField(null=True, blank=True) # models.ForeignKey(Ruleset, models.SET_NULL, blank=True, null=True)
    songList = models.IntegerField(null=True, blank=True) # should be some kind of list, need to figure this out