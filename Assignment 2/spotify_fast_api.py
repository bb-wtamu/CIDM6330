# Brandon Baither
# CIDM 6330
# Assignment 2

from typing import Optional, List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from enum import IntEnum

app = FastAPI()

# Pydantic models for my entities
# -------------------------------

class Tag(BaseModel):
    tagID: int
    name: str
    isNumeric: bool = Field(default=False)
    
class Song(BaseModel):
    songID: int
    artist: str
    title: str
    album: str
    spotifyURI: str
    tags: Dict[int, str] = Field(default={})

class SortStrategyEnum(IntEnum):
    ARTIST = 1
    TITLE = 2
    ALBUM = 3
    SHUFFLE = 4
    
class RequirementEnum(IntEnum):
    CONTAINS = 1
    NOT_CONTAINS = 2
    GREATER = 3
    LESS = 4
    EQUALS = 5

class Rule(BaseModel):
    tag: int
    requirement: RequirementEnum
    sort: SortStrategyEnum
    value: str
    count: int = Field(default=0)
    percent: float = Field(default=0.0)

class Ruleset(BaseModel):
    ruleSetID: int
    name: str
    songCount: int = Field(default=0)
    ruleList: List[Rule] = Field(default=[])
    
class Playlist(BaseModel):
    playlistID: int
    name: str
    spotifyID: str = Field(default="")
    generatedBy: Optional[Ruleset] = None
    songList: List[int] = Field(default=[])
    
# I have no idea how to implement a full database nicely using basic python datatypes. This got ugly in several places, but especially here.
# I didn't even try to implement the collection of users, since my dummy data would be 3-4 levels of nested dictionaries at that point.
class User(BaseModel):
    songLibrary: Dict[int, Song] = Field(default={})
    playlistLibrary: Dict[int, Playlist] = Field(default={})
    tagLibrary: Dict[int, Tag] = Field(default={})
    rulesetLibrary: Dict[int, Ruleset] = Field(default={})
    spotifyID: str

# dummy data from my pydantic models
# ----------------------------------

tags = {
    "1": Tag(tagID=1, name="Genre"),
    "2": Tag(tagID=2, name="Rating", isNumeric=True),
    "3": Tag(tagID=3, name="Mood"),
}

songs = {
    "1": Song(songID=1, artist="Pinkfong", title="Baby Shark", album="Baby Shark", spotifyURI="abcdefg1234567", tags={1: "Awesome", 2:"5"}),
    "2": Song(songID=2, artist="Rick Astley", title="Never Gonna Give You Up", album="Whenever You Need Somebody", spotifyURI="rickroll123", tags={1: "Memes", 2:"999", 3:"Joyous"}),
    "3": Song(songID=3, artist="Vitas", title="The 7th Element", album="Philosophy of Miracle", spotifyURI="hahaha13579", tags={3:"Party"}),
}

rules = {
    "1": Rule(tag=2, requirement=RequirementEnum.GREATER, sort=SortStrategyEnum.SHUFFLE, value="3", percent=.75),
    "2": Rule(tag=1, requirement=RequirementEnum.CONTAINS, sort=SortStrategyEnum.ARTIST, value="Awesome", percent=.25),
    "3": Rule(tag=3, requirement=RequirementEnum.NOT_CONTAINS, sort=SortStrategyEnum.SHUFFLE, value="Party", count=200),
}

rulesets = {
    "1": Ruleset(ruleSetID=1, name="Stuff", ruleList=[rules["1"],rules["2"]]),
    "2": Ruleset(ruleSetID=2, name="More Stuff", songCount=100, ruleList=[rules["1"], rules["3"]]),
    "3": Ruleset(ruleSetID=3, name="Even More Stuff", songCount=999, ruleList=[rules["2"]]),
}

playlists = {
    "1": Playlist(playlistID=1, name="Favorites", spotifyID="ziejvie39278", generatedBy=rulesets["2"], songList=[3,7,19,245,919,8,23]),
    "2": Playlist(playlistID=2, name="Working on it", generatedBy=None),
    "3": Playlist(playlistID=3, name="Some cool stuff", spotifyID="ienieuow9183", generatedBy=None, songList=[33,9812,82,777,12345]),
}

users = {
    "jim": User(songLibrary={1:songs["1"],2:songs["2"],3:songs["3"]}, playlistLibrary={1:playlists["1"],2:playlists["2"],3:playlists["3"]}, tagLibrary={1:tags["1"],2:tags["2"],3:tags["3"]}, rulesetLibrary={1:rulesets["1"],2:rulesets["2"],3:rulesets["3"]}, spotifyID="zzzzzzzzzzz"),
}

# CRUD operators
# --------------

# the getters

@app.get("/")
async def root():
    return {"message":"Welcome to the Spotify Playlist Generator API"}
    
@app.get("/getters/tags/{tag_id}")
def read_tags(tag_id: int):
    if str(tag_id) not in tags:
        raise HTTPException(status_code=404, detail="tag not found")
    return {"tag_id": tag_id, "tag": tags[str(tag_id)]}

@app.get("/getters/songs/{song_id}")
def read_songs(song_id: int):
    if str(song_id) not in songs:
        raise HTTPException(status_code=404, detail="song not found")
    return {"song_id": song_id, "song": songs[str(song_id)]}
    
@app.get("/getters/rules/{rule_id}")
def read_rules(rule_id: int):
    if str(rule_id) not in rules:
        raise HTTPException(status_code=404, detail="rule not found")
    return {"rule_id": rule_id, "rule": rules[str(rule_id)]}
    
@app.get("/getters/rulesets/{ruleset_id}")
def read_rulesets(ruleset_id: int):
    if str(ruleset_id) not in rulesets:
        raise HTTPException(status_code=404, detail="ruleset not found")
    return {"ruleset_id": ruleset_id, "ruleset": rulesets[str(ruleset_id)]}

@app.get("/getters/playlists/{playlist_id}")
def read_playlists(playlist_id: int):
    if str(playlist_id) not in playlists:
        raise HTTPException(status_code=404, detail="playlist not found")
    return {"playlist_id": playlist_id, "playlist": playlists[str(playlist_id)]}

@app.get("/getters/users/{user_id}")
def read_users(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="user not found")
    return {"user_id": user_id, "user": users[user_id]}


# the setters

@app.post("/setters/tags/{tag_id}")
def new_tags(tag_id: int, tag: Tag):
    if str(tag_id) in tags:
        raise HTTPException(status_code=400, detail="tag already exists")
    tags[str(tag_id)] = tag
    return {"tag_id": tag_id, "tag": tags[str(tag_id)]}

@app.post("/setters/songs/{song_id}")
def new_songs(song_id: int, song: Song):
    if str(song_id) in songs:
        raise HTTPException(status_code=400, detail="song already exists")
    songs[str(song_id)] = song
    return {"song_id": song_id, "song": songs[str(song_id)]}

@app.post("/setters/rules/{rule_id}")
def new_rules(rule_id: int, rule: Rule):
    if str(rule_id) in rules:
        raise HTTPException(status_code=400, detail="rule already exists")
    rules[str(rule_id)] = rule
    return {"rule_id": rule_id, "rule": rules[str(rule_id)]}

@app.post("/setters/rulesets/{ruleset_id}")
def new_rulesets(ruleset_id: int, ruleset: Ruleset):
    if str(ruleset_id) in rulesets:
        raise HTTPException(status_code=400, detail="ruleset already exists")
    rulesets[str(ruleset_id)] = ruleset
    return {"ruleset_id": ruleset_id, "ruleset": rulesets[str(ruleset_id)]}

@app.post("/setters/playlists/{playlist_id}")
def new_playlists(playlist_id: int, playlist: Playlist):
    if str(playlist_id) in playlists:
        raise HTTPException(status_code=400, detail="playlist already exists")
    playlists[str(playlist_id)] = playlist
    return {"playlist_id": playlist_id, "playlist": playlists[str(playlist_id)]}

@app.post("/setters/users/{user_id}")
def new_users(user_id: str, user: User):
    if user_id in users:
        raise HTTPException(status_code=400, detail="user already exists")
    users[user_id] = user
    return {"user_id": user_id, "user": users[user_id]}


# the fixers

@app.put("/fixers/tags/{tag_id}")
def mod_tags(tag_id: int, tag: Tag):
    if str(tag_id) not in tags:
        raise HTTPException(status_code=404, detail="tag not found")
    tags[str(tag_id)] = tag
    return {"tag_id": tag_id, "tag": tags[str(tag_id)]}

@app.put("/fixers/songs/{song_id}")
def mod_songs(song_id: int, song: Song):
    if str(song_id) not in songs:
        raise HTTPException(status_code=404, detail="song not found")
    songs[str(song_id)] = song
    return {"song_id": song_id, "song": songs[str(song_id)]}

@app.put("/fixers/rules/{rule_id}")
def mod_rules(rule_id: int, rule: Rule):
    if str(rule_id) not in rules:
        raise HTTPException(status_code=404, detail="rule not found")
    rules[str(rule_id)] = rule
    return {"rule_id": rule_id, "rule": rules[str(rule_id)]}

@app.put("/fixers/rulesets/{ruleset_id}")
def mod_rulesets(ruleset_id: int, ruleset: Ruleset):
    if str(ruleset_id) not in rulesets:
        raise HTTPException(status_code=404, detail="ruleset not found")
    rulesets[str(ruleset_id)] = ruleset
    return {"ruleset_id": ruleset_id, "ruleset": rulesets[str(ruleset_id)]}

@app.put("/fixers/playlists/{playlist_id}")
def mod_playlists(playlist_id: int, playlist: Playlist):
    if str(playlist_id) not in playlists:
        raise HTTPException(status_code=404, detail="playlist not found")
    playlists[str(playlist_id)] = playlist
    return {"playlist_id": playlist_id, "playlist": playlists[str(playlist_id)]}

@app.put("/fixers/users/{user_id}")
def mod_users(user_id: str, user: User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="user not found")
    users[user_id] = user
    return {"user_id": user_id, "user": users[user_id]}


# the wipers

@app.delete("/wipers/tags/{tag_id}")
def del_tags(tag_id: int):
    if str(tag_id) not in tags:
        raise HTTPException(status_code=404, detail="tag not found")
    return {"tag_id": tag_id, "tag": tags.pop(str(tag_id))}

@app.delete("/wipers/songs/{song_id}")
def del_songs(song_id: int):
    if str(song_id) not in songs:
        raise HTTPException(status_code=404, detail="song not found")
    return {"song_id": song_id, "song": songs.pop(str(song_id))}

@app.delete("/wipers/rules/{rule_id}")
def del_rules(rule_id: int):
    if str(rule_id) not in rules:
        raise HTTPException(status_code=404, detail="rule not found")
    return {"rule_id": rule_id, "rule": rules.pop(str(rule_id))}

@app.delete("/wipers/rulesets/{ruleset_id}")
def del_rulesets(ruleset_id: int):
    if str(ruleset_id) not in rulesets:
        raise HTTPException(status_code=404, detail="ruleset not found")
    return {"ruleset_id": ruleset_id, "ruleset": rulesets.pop(str(ruleset_id))}

@app.delete("/wipers/playlists/{playlist_id}")
def del_playlists(playlist_id: int):
    if str(playlist_id) not in playlists:
        raise HTTPException(status_code=404, detail="playlist not found")
    return {"playlist_id": playlist_id, "playlist": playlists.pop(str(playlist_id))}

@app.delete("/wipers/users/{user_id}")
def del_users(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="user not found")
    return {"user_id": user_id, "user": users.pop(user_id)}


# if you want to use uvicorn

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
