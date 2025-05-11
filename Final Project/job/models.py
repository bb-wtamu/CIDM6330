from django.db import models

class Song(models.Model):
    songID = models.AutoField(primary_key=True)
    artist = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    spotifyURI = models.CharField(max_length=200)
    
class Tag(models.Model):
    tagID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    isNumeric = models.booleanField()
    
class Tagged(models.Model):
    taggedID = models.AutoField(primary_key=True)
    song = models.ForeignKey(Song, models.CASCADE)
    tag = models.ForeignKey(Tag, models.CASCADE)
    value = models.CharField(max_length=70, null=True)
    value_num = models.IntegerField(null=True)
    
class Ruleset(models.Model):
    rulesetID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    songCount = models.IntegerField(null=True)
    
class Rule(models.Model):
    ARTIST = 1
    TITLE = 2
    ALBUM = 3
    SHUFFLE = 4
    SORT_STRATEGY_CHOICES = {
        ARTIST: "Artist",
        TITLE: "Title",
        ALBUM: "Album",
        SHUFFLE: "Shuffle",
    }
    
    CONTAINS = 1
    NOT_CONTAINS = 2
    GREATER = 3
    LESS = 4
    EQUALS = 5
    REQUIREMENT_CHOICES = {
        CONTAINS = "Contains",
        NOT_CONTAINS = "Does Not Contain",
        GREATER = "Greater Than",
        LESS = "Less Than",
        EQUALS = "Equal To",
    }
    
    ruleID = models.AutoField(primary_key=True)
    tag = models.ForeignKey(Tag, models.CASCADE)
    ruleset = models.ForeignKey(Ruleset, models.CASCADE)
    requirement = models.IntegerField(choices=REQUIREMENT_CHOICES)
    sort_strategy = models.IntegerField(choices=SORT_STRATEGY_CHOICES)
    threshold = models.IntegerField(null=True)
    value = models.CharField(max_length=70, null=True)
    count = models.IntegerField()
    percent = models.DecimalField(max_digits=4, decimal_places=2)

class Playlist(models.Model):
    playlistID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    spotifyID = models.CharField(max_length=200)
    generatedBy = models.ForeignKey(Ruleset, models.SET_NULL, null=True)
    
class PlaylistAssignment(models.Model):
    playlistAssignmentID = models.AutoField(primary_key=True)
    song = models.ForeignKey(Song, models.CASCADE)
    playlist = models.ForeignKey(Playlist, models.CASCADE)
    position = models.IntegerField()
    
class User(models.Model):
    userID = models.AutoField(primary_key=True)
    spotifyID = models.CharField(max_length=200)
    songLibrary = models.ManyToManyField(Song)
    playlistLibrary = models.ManyToManyField(Playlist)
    tagLibrary = models.ManyToManyField(Tag)
    rulesetLibrary = models.ManyToManyField(Ruleset)