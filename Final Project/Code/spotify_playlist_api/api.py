from django.shortcuts import get_object_or_404

from ninja import NinjaAPI, Schema, Router, Field
from job.api import router as alt_router
from typing import List

from job.models import Song
from job.models import Tag
from job.models import Tagged
from job.models import Ruleset
from job.models import Rule
from job.models import Playlist
from job.models import PlaylistAssignment
from job.models import User

#------ SCHEMAS
class SongIn(Schema):
    artist: str
    title: str
    album: str
    spotifyURI: str
    tags: str

class SongOut(Schema):
    songID: int
    artist: str
    title: str
    album: str
    spotifyURI: str
    tags: str
    
class TagIn(Schema):
    name: str
    isNumeric: bool
    
class TagOut(Schema):
    tagID: int
    name: str
    isNumeric: bool
    
class TaggedIn(Schema):
    song_id: int
    tag_id: int
    value: str
    value_num: int
    
class TaggedOut(Schema):
    taggedID: int
    song_id: int
    tag_id: int
    value: str
    value_num: int
    
class RulesetIn(Schema):
    name: str
    songCount: int
    
class RulesetOut(Schema):
    rulesetID: int
    name: str
    songCount: int
    
class RuleIn(Schema):
    tag_id: int
    song_id: int
    requirement: int
    sort_strategy: int
    threshold: int
    value: str
    count: int
    percent: float
    
class RuleOut(Schema):
    ruleID: int
    tag_id: int
    song_id: int
    requirement: int
    sort_strategy: int
    threshold: int
    value: str
    count: int
    percent: float

class PlaylistIn(Schema):
    name: str
    spotifyID: str
    generatedBy_id: int

class PlaylistOut(Schema):
    playlistID: int
    name: str
    spotifyID: str
    generatedBy_id: int
    
class PlaylistAssignmentIn(Schema):
    song_id: int
    playlist_id: int
    position: int
    
class PlaylistAssignmentOut(Schema):
    playlistAssignmentID: int
    song_id: int
    playlist_id: int
    position: int
    
class UserIn(Schema):
    spotifyID: str
    
class UserOut(Schema):
    userID: int
    spotifyID: str

#------ API SETUP

api = NinjaAPI()
api.add_router("/import/", alt_router)

# SONG

@api.post("/song")
def create_song(request, song: SongIn):
    newSong = Song.objects.create(**song.dict())
    return newSong

@api.get("/song/{song_id}", response=SongOut)
def get_song(request, song_id: int):
    song = get_object_or_404(Song, songID=song_id)
    return song

@api.get("/song", response=list[SongOut])
def list_songs(request):
    songs = Song.objects.all()
    return songs

@api.put("/song/{song_id}")
def update_song(request, song_id: int, payload: SongIn):
    song = get_object_or_404(Song, songID=song_id)
    for attr, value in payload.dict().items():
        setattr(song, attr, value)
    song.save()
    return {"success": True, "song": song}

@api.delete("/song/{song_id}")
def delete_song(request, song_id: int):
    song = get_object_or_404(Song, songID=song_id)
    song.delete()
    return {"success": True, "song": song}
    
# TAG

@api.post("/tag")
def create_tag(request, tag: TagIn):
    newTag = Tag.objects.create(**tag.dict())
    return newTag

@api.get("/tag/{tag_id}", response=TagOut)
def get_tag(request, tag_id: int):
    tag = get_object_or_404(Tag, tagID=tag_id)
    return tag

@api.get("/tag", response=list[TagOut])
def list_tags(request):
    tags = Tag.objects.all()
    return tags

@api.put("/tag/{tag_id}")
def update_tag(request, tag_id: int, payload: TagIn):
    tag = get_object_or_404(Tag, tagID=tag_id)
    for attr, value in payload.dict().items():
        setattr(tag, attr, value)
    tag.save()
    return {"success": True, "tag": tag}

@api.delete("/tag/{tag_id}")
def delete_tag(request, tag_id: int):
    tag = get_object_or_404(Tag, tagID=tag_id)
    tag.delete()
    return {"success": True, "tag": tag}
    
# TAGGED

@api.post("/tagged")
def create_tagged(request, tagged: TaggedIn):
    newTagged = Tagged.objects.create(**tagged.dict())
    return newTagged

@api.get("/tagged/{tagged_id}", response=TaggedOut)
def get_tagged(request, tagged_id: int):
    tagged = get_object_or_404(Tagged, taggedID=tagged_id)
    return tagged

@api.get("/tagged", response=list[TaggedOut])
def list_taggeds(request):
    taggeds = Tagged.objects.all()
    return taggeds

@api.put("/tagged/{tagged_id}")
def update_tagged(request, tagged_id: int, payload: TaggedIn):
    tagged = get_object_or_404(Tagged, taggedID=tagged_id)
    for attr, value in payload.dict().items():
        setattr(tagged, attr, value)
    tagged.save()
    return {"success": True, "tagged": tagged}

@api.delete("/tagged/{tagged_id}")
def delete_tagged(request, tagged_id: int):
    tagged = get_object_or_404(Tagged, taggedID=tagged_id)
    tagged.delete()
    return {"success": True, "tagged": tagged}
    
# RULESET

@api.post("/ruleset")
def create_ruleset(request, ruleset: RulesetIn):
    newRuleset = Ruleset.objects.create(**ruleset.dict())
    return newRuleset

@api.get("/ruleset/{ruleset_id}", response=RulesetOut)
def get_ruleset(request, ruleset_id: int):
    ruleset = get_object_or_404(Ruleset, rulesetID=ruleset_id)
    return ruleset

@api.get("/ruleset", response=list[RulesetOut])
def list_rulesets(request):
    rulesets = Ruleset.objects.all()
    return rulesets

@api.put("/ruleset/{ruleset_id}")
def update_ruleset(request, ruleset_id: int, payload: RulesetIn):
    ruleset = get_object_or_404(Ruleset, rulesetID=ruleset_id)
    for attr, value in payload.dict().items():
        setattr(ruleset, attr, value)
    ruleset.save()
    return {"success": True, "ruleset": ruleset}

@api.delete("/ruleset/{ruleset_id}")
def delete_ruleset(request, ruleset_id: int):
    ruleset = get_object_or_404(Ruleset, rulesetID=ruleset_id)
    ruleset.delete()
    return {"success": True, "ruleset": ruleset}
    
# RULE

@api.post("/rule")
def create_rule(request, rule: RuleIn):
    newRule = Rule.objects.create(**rule.dict())
    return newRule

@api.get("/rule/{rule_id}", response=RuleOut)
def get_rule(request, rule_id: int):
    rule = get_object_or_404(Rule, ruleID=rule_id)
    return rule

@api.get("/rule", response=list[RuleOut])
def list_rules(request):
    rules = Rule.objects.all()
    return rules

@api.put("/rule/{rule_id}")
def update_rule(request, rule_id: int, payload: RuleIn):
    rule = get_object_or_404(Rule, ruleID=rule_id)
    for attr, value in payload.dict().items():
        setattr(rule, attr, value)
    rule.save()
    return {"success": True, "rule": rule}

@api.delete("/rule/{rule_id}")
def delete_rule(request, rule_id: int):
    rule = get_object_or_404(Rule, ruleID=rule_id)
    rule.delete()
    return {"success": True, "rule": rule}

# PLAYLIST

@api.post("/playlist")
def create_playlist(request, playlist: PlaylistIn):
    Playlist.objects.create(**playlist.dict())
    return playlist

@api.get("/playlist/{playlist_id}", response=PlaylistOut)
def get_playlist(request, playlist_id: int):
    playlist = get_object_or_404(Playlist, playlistID=playlist_id)
    return playlist

@api.get("/playlist", response=list[PlaylistOut])
def list_playlists(request):
    playlists = Playlist.objects.all()
    return playlists

@api.put("/playlist/{playlist_id}")
def update_playlist(request, playlist_id: int, payload: PlaylistIn):
    playlist = get_object_or_404(Playlist, playlistID=playlist_id)
    for attr, value in payload.dict().items():
        setattr(playlist, attr, value)
    playlist.save()
    return {"success": True, "playlist": playlist}

@api.delete("/playlist/{playlist_id}")
def delete_playlist(request, playlist_id: int):
    playlist = get_object_or_404(Playlist, playlistID=playlist_id)
    playlist.delete()
    return {"success": True, "playlist": playlist}
    
# PLAYLISTASSIGNMENT

@api.post("/playlistassignment")
def create_playlistassignment(request, playlistassignment: PlaylistAssignmentIn):
    newPlaylistAssignment = PlaylistAssignment.objects.create(**playlistassignment.dict())
    return newPlaylistAssignment

@api.get("/playlistassignment/{playlistassignment_id}", response=PlaylistAssignmentOut)
def get_playlistassignment(request, playlistassignment_id: int):
    playlistassignment = get_object_or_404(PlaylistAssignment, playlistAssignmentID=playlistassignment_id)
    return playlistassignment

@api.get("/playlistassignment", response=list[PlaylistAssignmentOut])
def list_playlistassignments(request):
    playlistassignments = PlaylistAssignment.objects.all()
    return playlistassignments

@api.put("/playlistassignment/{playlistassignment_id}")
def update_playlistassignment(request, playlistassignment_id: int, payload: PlaylistAssignmentIn):
    playlistassignment = get_object_or_404(PlaylistAssignment, playlistAssignmentID=playlistassignment_id)
    for attr, value in payload.dict().items():
        setattr(playlistassignment, attr, value)
    playlistassignment.save()
    return {"success": True, "playlistassignment": playlistassignment}

@api.delete("/playlistassignment/{playlistassignment_id}")
def delete_playlistassignment(request, playlistassignment_id: int):
    playlistassignment = get_object_or_404(PlaylistAssignment, playlistAssignmentID=playlistassignment_id)
    playlistassignment.delete()
    return {"success": True, "playlistassignment": playlistassignment}
    
# USER

@api.post("/user")
def create_user(request, user: UserIn):
    newUser = User.objects.create(**user.dict())
    return newUser

@api.get("/user/{user_id}", response=UserOut)
def get_user(request, user_id: int):
    user = get_object_or_404(User, userID=user_id)
    return user

@api.get("/user", response=list[UserOut])
def list_users(request):
    users = User.objects.all()
    return users

@api.put("/user/{user_id}")
def update_user(request, user_id: int, payload: UserIn):
    user = get_object_or_404(User, userID=user_id)
    for attr, value in payload.dict().items():
        setattr(user, attr, value)
    user.save()
    return {"success": True, "user": user}

@api.delete("/user/{user_id}")
def delete_user(request, user_id: int):
    user = get_object_or_404(User, userID=user_id)
    user.delete()
    return {"success": True, "user": user}
    

#-------------- Complex, non-CRUD
@api.post("/addToPlaylist")
def add_to_playlist(request, playlist: int, songs: List[int]):
    for index, song in enumerate(songs):
        PlaylistAssignment.objects.create(song_id = song, playlist_id = playlist, position=index)
    return get_object_or_404(Playlist, playlistID=playlist)
    
@api.post("/tagSongs")
def tag_songs(request, setTag_id: int, val: str, val_int: int, songs: List[int]):
    tag = get_object_or_404(Tag, tagID=setTag_id)
    for song in songs:
        if tag.isNumeric:
            Tagged.objects.create(song_id=song, tag_id=setTag_id, value_num=val_int)
        else:
            Tagged.objects.create(song_id=song, tag_id=setTag_id, value=val)
    return tag
    
@api.put("/user/songs/{user_id}")
def associate_songs_to_user(request, user_id: int, songs: List[int]):
    user = get_object_or_404(User, userID=user_id)
    for song in songs:
        user.songLibrary.add(get_object_or_404(Song, songID=song))
    return user
    
@api.put("/user/playlists/{user_id}")
def associate_playlists_to_user(request, user_id: int, playlists: List[int]):
    user = get_object_or_404(User, userID=user_id)
    for playlist in playlists:
        user.playlistLibrary.add(get_object_or_404(Playlist, playlistID=playlist))
    return user
    
@api.put("/user/tags/{user_id}")
def associate_tags_to_user(request, user_id: int, tags: List[int]):
    user = get_object_or_404(User, userID=user_id)
    for tag in tags:
        user.tagLibrary.add(get_object_or_404(Tag, tagID=tag))
    return user
    
@api.put("/user/rulesets/{user_id}")
def associate_rulesets_to_user(request, user_id: int, rulesets: List[int]):
    user = get_object_or_404(User, userID=user_id)
    for ruleset in rulesets:
        user.rulesetLibrary.add(get_object_or_404(Ruleset, rulesetID=ruleset))
    return user