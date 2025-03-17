# Brandon Baither
# CIDM 6330
# Assignment 2

from typing import Optional, List, Dict
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from enum import IntEnum
from abc import ABC, abstractmethod
import traceback
import csv
from dataclasses import dataclass, asdict, field, InitVar

app = FastAPI()

# Pydantic models for my entities
# -------------------------------

@dataclass
class Tag(SQLModel, table=True):
    tagID: int = Field(default=None, primary_key=True)
    name: str
    isNumeric: bool = Field(default=False)

@dataclass    
class Song(SQLModel, table=True):
    songID: int = Field(default=None, primary_key=True)
    artist: str
    title: str
    album: str
    spotifyURI: str
    tags: str           # tags: Dict[int, str] = Field(default={})

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

@dataclass
class Rule(SQLModel, table=True):
    ruleID: int = Field(default=None, primary_key=True)
    tag: int
    requirement: RequirementEnum
    sort: SortStrategyEnum
    value: str
    count: int = Field(default=0)
    percent: float = Field(default=0.0)

@dataclass
class Ruleset(SQLModel, table=True):
    ruleSetID: int = Field(default=None, primary_key=True)
    name: str
    songCount: int = Field(default=0)
    ruleList: str     #   List[Rule] = Field(default=[])

@dataclass
class Playlist(SQLModel, table=True):
    playlistID: int = Field(default=None, primary_key=True)
    name: str
    spotifyID: str = Field(default="")
    generatedBy: Optional[int] = None
    songList: int     #    List[int] = Field(default=[])
    
# I have no idea how to implement a full database nicely using basic python datatypes. This got ugly in several places, but especially here.
# I didn't even try to implement the collection of users, since my dummy data would be 3-4 levels of nested dictionaries at that point.
@dataclass
class User(SQLModel, table=True):
    userID: int = Field(default=None, primary_key=True)
    songLibrary: int #   Dict[int, Song] = Field(default={})
    playlistLibrary: int #   Dict[int, Playlist] = Field(default={})
    tagLibrary: int    #   Dict[int, Tag] = Field(default={})
    rulesetLibrary: int     #   Dict[int, Ruleset] = Field(default={})
    spotifyID: str

# dummy data from my pydantic models
# ----------------------------------

tags = {
    "1": Tag(tagID=1, name="Genre"),
    "2": Tag(tagID=2, name="Rating", isNumeric=True),
    "3": Tag(tagID=3, name="Mood"),
}

songs = {
    "1": Song(songID=1, artist="Pinkfong", title="Baby Shark", album="Baby Shark", spotifyURI="abcdefg1234567", tags="fakeTag"),    # {1: "Awesome", 2:"5"}),
    "2": Song(songID=2, artist="Rick Astley", title="Never Gonna Give You Up", album="Whenever You Need Somebody", spotifyURI="rickroll123", tags="blahTag"),      #    {1: "Memes", 2:"999", 3:"Joyous"}),
    "3": Song(songID=3, artist="Vitas", title="The 7th Element", album="Philosophy of Miracle", spotifyURI="hahaha13579", tags="funTag"),      #   {3:"Party"}),
}

rules = {
    "1": Rule(ruleID=1, tag=2, requirement=RequirementEnum.GREATER, sort=SortStrategyEnum.SHUFFLE, value="3", percent=.75),
    "2": Rule(ruleID=2, tag=1, requirement=RequirementEnum.CONTAINS, sort=SortStrategyEnum.ARTIST, value="Awesome", percent=.25),
    "3": Rule(ruleID=3, tag=3, requirement=RequirementEnum.NOT_CONTAINS, sort=SortStrategyEnum.SHUFFLE, value="Party", count=200),
}

rulesets = {
    "1": Ruleset(ruleSetID=1, name="Stuff", ruleList="rule1"),   #  [rules["1"],rules["2"]]),
    "2": Ruleset(ruleSetID=2, name="More Stuff", songCount=100, ruleList="rule3"),    #  [rules["1"], rules["3"]]),
    "3": Ruleset(ruleSetID=3, name="Even More Stuff", songCount=999, ruleList="rule2"),    #  [rules["2"]]),
}

playlists = {
    "1": Playlist(playlistID=1, name="Favorites", spotifyID="ziejvie39278", generatedBy=None, songList=5),   #   [3,7,19,245,919,8,23]),
    "2": Playlist(playlistID=2, name="Working on it", generatedBy=None, songList=237),
    "3": Playlist(playlistID=3, name="Some cool stuff", spotifyID="ienieuow9183", generatedBy=None, songList=234),    #   [33,9812,82,777,12345]),
}

users = {
    "1": User(userID = 1, songLibrary = 7, playlistLibrary = 987, tagLibrary = 55, rulesetLibrary = 853, spotifyID="zzzzzzzzz"),
    #    "jim": User(userID = 1, songLibrary={1:songs["1"],2:songs["2"],3:songs["3"]}, playlistLibrary={1:playlists["1"],2:playlists["2"],3:playlists["3"]}, tagLibrary={1:tags["1"],2:tags["2"],3:tags["3"]}, rulesetLibrary={1:rulesets["1"],2:rulesets["2"],3:rulesets["3"]}, spotifyID="zzzzzzzzzzz"),
}


# Abstract Repository
#--------------------
class BaseSpotifyRepo(ABC):
    
    # the getters
    @abstractmethod
    def read_tags_repo(self, tag_id: int):
        pass
    
    @abstractmethod
    def read_songs_repo(self, song_id: int):
        pass
        
    @abstractmethod    
    def read_rules_repo(self, rule_id: int):
        pass
        
    @abstractmethod
    def read_rulesets_repo(self, ruleset_id: int):
        pass
        
    @abstractmethod
    def read_playlists_repo(self, playlist_id: int):
        pass
        
    @abstractmethod
    def read_users_repo(self, user_id: str):
        pass
        

    # the setters
    @abstractmethod
    def new_tags_repo(self, tag: Tag):
        pass
        
    @abstractmethod
    def new_songs_repo(self, song: Song):
        pass
        
    @abstractmethod
    def new_rules_repo(self, rule: Rule):
        pass
    
    @abstractmethod
    def new_rulesets_repo(self, ruleset: Ruleset):
        pass
    
    @abstractmethod
    def new_playlists_repo(self, playlist: Playlist):
        pass
        
    @abstractmethod
    def new_users_repo(self, user: User):
        pass


    # the fixers
    @abstractmethod
    def mod_tags_repo(self, tag_id: int, field, value):
        pass
        
    @abstractmethod
    def mod_songs_repo(self, song_id: int, field, value):
        pass
        
    @abstractmethod
    def mod_rules_repo(self, rule_id: int, field, value):
        pass
        
    @abstractmethod
    def mod_rulesets_repo(self, ruleset_id: int, field, value):
        pass
        
    @abstractmethod
    def mod_playlists_repo(self, playlist_id: int, field, value):
        pass
        
    @abstractmethod
    def mod_users_repo(self, user_id: str, field, value):
        pass


    # the wipers
    @abstractmethod
    def del_tags_repo(self, tag_id: int):
        pass
        
    @abstractmethod
    def del_songs_repo(self, song_id: int):
        pass
        
    @abstractmethod
    def del_rules_repo(self, rule_id: int):
        pass
        
    @abstractmethod
    def del_rulesets_repo(self, ruleset_id: int):
        pass
        
    @abstractmethod
    def del_playlists_repo(self, playlist_id: int):
        pass
        
    @abstractmethod
    def del_users_repo(self, user_id: str):
        pass
        

class SpotifySQLModelRepo(BaseSpotifyRepo):
    """
    Works with SQL Model, which is a library that provides a way to work with SQL databases in Python.
    """

    def __init__(self, db_string="sqlite:///spotify.db"):
        # ability to work use the database
        self.engine = create_engine(db_string)
        # ability to create all tables and structures
        SQLModel.metadata.create_all(self.engine)
        # ability to perform operations on the database
        self.session = Session(self.engine)
        
        # the getters
    def read_tags_repo(self, tag_id: int):
        statement = select(Tag).where(Tag.tagID == tag_id)
        result = self.session.exec(statement)
        return result.one()
    
    def read_songs_repo(self, song_id: int):
        statement = select(Song).where(Song.songID == song_id)
        result = self.session.exec(statement)
        return result.one()
        
    def read_rules_repo(self, rule_id: int):
        statement = select(Rule).where(Rule.ruleID == rule_id)
        result = self.session.exec(statement)
        return result.one()

    def read_rulesets_repo(self, ruleset_id: int):
        statement = select(Ruleset).where(Ruleset.ruleSetID == ruleset_id)
        result = self.session.exec(statement)
        return result.one()

    def read_playlists_repo(self, playlist_id: int):
        statement = select(Playlist).where(Playlist.playlistID == playlist_id)
        result = self.session.exec(statement)
        return result.one()

    def read_users_repo(self, user_id: str):
        statement = select(User).where(User.userID == user_id)
        result = self.session.exec(statement)
        return result.one()
        

    # the setters
    def new_tags_repo(self, tag: Tag):
        self.session.add(tag)
        self.session.commit()

    def new_songs_repo(self, song: Song):
        self.session.add(song)
        self.session.commit()

    def new_rules_repo(self, rule: Rule):
        self.session.add(rule)
        self.session.commit()

    def new_rulesets_repo(self, ruleset: Ruleset):
        self.session.add(ruleset)
        self.session.commit()

    def new_playlists_repo(self, playlist: Playlist):
        self.session.add(playlist)
        self.session.commit()

    def new_users_repo(self, user: User):
        self.session.add(user)
        self.session.commit()


    # the fixers
    def mod_tags_repo(self, tag_id: int, field, value):
        tag = self.read_tags_repo(tag_id)
        
        if field == "name":
            tag.name = value
        
        if field == "isNumeric":
            tag.isNumeric = value
            
        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)

    def mod_songs_repo(self, song_id: int, field, value):
        song = self.read_songs_repo(song_id)
        
        if field == "artist":
            song.artist = value
            
        if field == "title":
            song.title = value
            
        if field == "album":
            song.album = value
            
        if field == "spotifyURI":
            song.spotifyURI = value
            
        if field == "tags":
            song.tags = value
            
        self.session.add(song)
        self.session.commit()
        self.session.refresh(song)

    def mod_rules_repo(self, rule_id: int, field, value):
        rule = self.read_rules_repo(rule_id)
        
        if field == "tag":
            rule.tag = value
            
        if field == "requirement":
            rule.requirement = value
            
        if field == "sort":
            rule.sort = value
            
        if field == "value":
            rule.value = value
            
        if field == "count":
            rule.count = value
            
        if field == "percent":
            rule.percent = value
            
        self.session.add(rule)
        self.session.commit()
        self.session.refresh(rule)

    def mod_rulesets_repo(self, ruleset_id: int, field, value):
        rs = self.read_rulesets_repo(ruleset_id)
        
        if field == "name":
            rs.name = value
            
        if field == "songCount":
            rs.songCount = value
            
        if field == "ruleList":
            rs.ruleList = value
            
        self.session.add(rs)
        self.session.commit()
        self.session.refresh(rs)

    def mod_playlists_repo(self, playlist_id: int, field, value):
        pl = self.read_playlists_repo(playlist_id)
        
        if field == "name":
            pl.name = value
            
        if field == "spotifyID":
            pl.spotifyID = value
            
        if field == "generatedBy":
            pl.generatedBy = value
            
        if field == "songList":
            pl.songList = value
            
        self.session.add(pl)
        self.session.commit()
        self.session.refresh(pl)

    def mod_users_repo(self, user_id: str, field, value):
        user = self.read_users_repo(user_id)
        
        if field == "songLibrary":
            user.songLibrary = value
            
        if field == "playlistLibrary":
            user.playlistLibrary = value
            
        if field == "tagLibrary":
            user.tagLibrary = value
            
        if field == "rulesetLibrary":
            user.rulesetLibrary = value
            
        if field == "spotifyID":
            user.spotifyID = value
            
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)


    # the wipers
    def del_tags_repo(self, tag_id: int):
        tag = self.read_tags_repo(tag_id)
        self.session.delete(tag)
        self.session.commit()
        
    def del_songs_repo(self, song_id: int):
        song = self.read_songs_repo(song_id)
        self.session.delete(song)
        self.session.commit()

    def del_rules_repo(self, rule_id: int):
        rule = self.read_rules_repo(rule_id)
        self.session.delete(rule)
        self.session.commit()

    def del_rulesets_repo(self, ruleset_id: int):
        rs = self.read_rulesets_repo(ruleset_id)
        self.session.delete(rs)
        self.session.commit()

    def del_playlists_repo(self, playlist_id: int):
        pl = self.read_playlists_repo(playlist_id)
        self.session.delete(pl)
        self.session.commit()

    def del_users_repo(self, user_id: str):
        user = self.read_users_repo(user_id)
        self.session.delete(user)
        self.session.commit()


class SpotifyCSVRepo(BaseSpotifyRepo):
    """
    Note: CSV files don’t maintain data types. All field values are considered str and empty values are considered None.
    """

    def __init__(self, tagFilename: str, tagFieldnames: list, songFilename: str, songFieldnames: list, ruleFilename: str, ruleFieldnames: list, rulesetFilename: str, rulesetFieldnames: list, playlistFilename: str, playlistFieldnames: list, userFilename: str, userFieldnames: list):
        self.tagRepo = []
        self.tagFilename = tagFilename
        self.tagFieldnames = tagFieldnames
        
        self.songRepo = []
        self.songFilename = songFilename
        self.songFieldnames = songFieldnames
        
        self.ruleRepo = []
        self.ruleFilename = ruleFilename
        self.ruleFieldnames = ruleFieldnames
        
        self.rulesetRepo = []
        self.rulesetFilename = rulesetFilename
        self.rulesetFieldnames = rulesetFieldnames
        
        self.playlistRepo = []
        self.playlistFilename = playlistFilename
        self.playlistFieldnames = playlistFieldnames
        
        self.userRepo = []
        self.userFilename = userFilename
        self.userFieldnames = userFieldnames

        try:
            with open(tagFilename, mode="r", newline="") as file:
                csv_reader = csv.DictReader(file)
                # list comprehension: https://www.w3schools.com/python/python_lists_comprehension.asp
                self.tagRepo = [Tag(**row) for row in csv_reader]
        except Exception as error:
            print("Exception in file open: ", error)

        try:
            with open(songFilename, mode="r", newline="") as file:
                csv_reader = csv.DictReader(file)
                self.songRepo = [Song(**row) for row in csv_reader]
        except Exception as error:
            print("Exception in file open: ", error)
            
        try:
            with open(ruleFilename, mode="r", newline="") as file:
                csv_reader = csv.DictReader(file)
                self.ruleRepo = [Rule(**row) for row in csv_reader]
        except Exception as error:
            print("Exception in file open: ", error)
            
        try:
            with open(rulesetFilename, mode="r", newline="") as file:
                csv_reader = csv.DictReader(file)
                self.rulesetRepo = [Ruleset(**row) for row in csv_reader]
        except Exception as error:
            print("Exception in file open: ", error)
            
        try:
            with open(playlistFilename, mode="r", newline="") as file:
                csv_reader = csv.DictReader(file)
                self.playlistRepo = [Playlist(**row) for row in csv_reader]
        except Exception as error:
            print("Exception in file open: ", error)
            
        try:
            with open(userFilename, mode="r", newline="") as file:
                csv_reader = csv.DictReader(file)
                self.userRepo = [User(**row) for row in csv_reader]
        except Exception as error:
            print("Exception in file open: ", error)
        
        # the getters
    def read_tags_repo(self, tag_id: int):
        for tag in self.tagRepo:
            if tag.tagID == tag_id:
                return tag
    
    def read_songs_repo(self, song_id: int):
        for song in self.songRepo:
            if song.songID == song_id:
                return song
        
    def read_rules_repo(self, rule_id: int):
        for rule in self.ruleRepo:
            if rule.ruleID == rule_id:
                return rule

    def read_rulesets_repo(self, ruleset_id: int):
        for rs in self.rulesetRepo:
            if rs.ruleSetID == ruleset_id:
                return rs

    def read_playlists_repo(self, playlist_id: int):
        for pl in self.playlistRepo:
            if pl.playlistID == playlist_id:
                return pl

    def read_users_repo(self, user_id: str):
        for user in self.userRepo:
            if user.userID == user_id:
                return user
        

    # the setters
    def new_tags_repo(self, tag: Tag):
        self.tagRepo.append(tag)
        self.save_tag_file()

    def new_songs_repo(self, song: Song):
        self.songRepo.append(song)
        self.save_song_file()

    def new_rules_repo(self, rule: Rule):
        self.ruleRepo.append(rule)
        self.save_rule_file()

    def new_rulesets_repo(self, ruleset: Ruleset):
        self.rulesetRepo.append(ruleset)
        self.save_ruleset_file()

    def new_playlists_repo(self, playlist: Playlist):
        self.playlistRepo.append(playlist)
        self.save_playlist_file()

    def new_users_repo(self, user: User):
        self.userRepo.append(user)
        self.save_user_file()


    # the fixers
    def mod_tags_repo(self, tag_id: int, field, value):        
        if field == "name":
            for index, tag in enumerate(self.tagRepo):
                if tag.tagID == tag_id:
                    tag.name = value
                    self.tagRepo[index] = tag
        
        if field == "isNumeric":
            for index, tag in enumerate(self.tagRepo):
                if tag.tagID == tag_id:
                    tag.isNumeric = value
                    self.tagRepo[index] = tag
                    
        self.save_tag_file()
        return tag

    def mod_songs_repo(self, song_id: int, field, value):
        if field == "artist":
            for index, song in enumerate(self.songRepo):
                if song.songID == song_id:
                    song.artist = value
                    self.songRepo[index] = song
            
        if field == "title":
            for index, song in enumerate(self.songRepo):
                if song.songID == song_id:
                    song.title = value
                    self.songRepo[index] = song
            
        if field == "album":
            for index, song in enumerate(self.songRepo):
                if song.songID == song_id:
                    song.album = value
                    self.songRepo[index] = song
            
        if field == "spotifyURI":
            for index, song in enumerate(self.songRepo):
                if song.songID == song_id:
                    song.spotifyURI = value
                    self.songRepo[index] = song
            
        if field == "tags":
            for index, song in enumerate(self.songRepo):
                if song.songID == song_id:
                    song.tags = value
                    self.songRepo[index] = song
            
        self.save_song_file()
        return song

    def mod_rules_repo(self, rule_id: int, field, value):
        if field == "tag":
            for index, rule in enumerate(self.ruleRepo):
                if rule.ruleID == rule_id:
                    rule.tag = value
                    self.ruleRepo[index] = rule
            
        if field == "requirement":
            for index, rule in enumerate(self.ruleRepo):
                if rule.ruleID == rule_id:
                    rule.requirement = value
                    self.ruleRepo[index] = rule
            
        if field == "sort":
            for index, rule in enumerate(self.ruleRepo):
                if rule.ruleID == rule_id:
                    rule.sort = value
                    self.ruleRepo[index] = rule
            
        if field == "value":
            for index, rule in enumerate(self.ruleRepo):
                if rule.ruleID == rule_id:
                    rule.value = value
                    self.ruleRepo[index] = rule
            
        if field == "count":
            for index, rule in enumerate(self.ruleRepo):
                if rule.ruleID == rule_id:
                    rule.count = value
                    self.ruleRepo[index] = rule
            
        if field == "percent":
            for index, rule in enumerate(self.ruleRepo):
                if rule.ruleID == rule_id:
                    rule.percent = value
                    self.ruleRepo[index] = rule
            
        self.save_rule_file()
        return fule

    def mod_rulesets_repo(self, ruleset_id: int, field, value):
        if field == "name":
            for index, rs in enumerate(self.rulesetRepo):
                if rs.ruleSetID == ruleset_id:
                    rs.name = value
                    self.rulesetRepo[index] = rs
            
        if field == "songCount":
            for index, rs in enumerate(self.rulesetRepo):
                if rs.ruleSetID == ruleset_id:
                    rs.songCount = value
                    self.rulesetRepo[index] = rs
            
        if field == "ruleList":
            for index, rs in enumerate(self.rulesetRepo):
                if rs.ruleSetID == ruleset_id:
                    rs.ruleList = value
                    self.rulesetRepo[index] = rs
            
        self.save_ruleset_file()
        return rs

    def mod_playlists_repo(self, playlist_id: int, field, value):
        if field == "name":
            for index, pl in enumerate(self.playlistRepo):
                if pl.playlistID == playlist_id:
                    pl.name = value
                    self.playlistRepo[index] = pl
            
        if field == "spotifyID":
            for index, pl in enumerate(self.playlistRepo):
                if pl.playlistID == playlist_id:
                    pl.spotifyID = value
                    self.playlistRepo[index] = pl
            
        if field == "generatedBy":
            for index, pl in enumerate(self.playlistRepo):
                if pl.playlistID == playlist_id:
                    pl.generatedBy = value
                    self.playlistRepo[index] = pl
            
        if field == "songList":
            for index, pl in enumerate(self.playlistRepo):
                if pl.playlistID == playlist_id:
                    pl.songList = value
                    self.playlistRepo[index] = pl
            
        self.save_playlist_file()
        return pl

    def mod_users_repo(self, user_id: str, field, value):
        if field == "songLibrary":
            for index, user in enumerate(self.userRepo):
                if user.userID == user_id:
                    user.songLibrary = value
                    self.userRepo[index] = user
            
        if field == "playlistLibrary":
            for index, user in enumerate(self.userRepo):
                if user.userID == user_id:
                    user.playlistLibrary = value
                    self.userRepo[index] = user
            
        if field == "tagLibrary":
            for index, user in enumerate(self.userRepo):
                if user.userID == user_id:
                    user.tagLibrary = value
                    self.userRepo[index] = user
            
        if field == "rulesetLibrary":
            for index, user in enumerate(self.userRepo):
                if user.userID == user_id:
                    user.rulesetLibrary = value
                    self.userRepo[index] = user
            
        if field == "spotifyID":
            for index, user in enumerate(self.userRepo):
                if user.userID == user_id:
                    user.spotifyID = value
                    self.userRepo[index] = user
            
        self.save_user_file()
        return user


    # the wipers
    def del_tags_repo(self, tag_id: int):
        for tag in self.tagRepo:
            if int(tag.tagID) == tag_id:
                self.tagRepo.remove(tag)
 
        self.save_tag_file()
        return tag
        
    def del_songs_repo(self, song_id: int):
        for song in self.songRepo:
            if int(song.songID) == song_id:
                self.songRepo.remove(song)
                
        self.save_song_file()
        return song

    def del_rules_repo(self, rule_id: int):
        for rule in self.ruleRepo:
            if int(rule.ruleID) == rule_id:
                self.ruleRepo.remove(rule)
                
        self.save_rule_file()
        return rule

    def del_rulesets_repo(self, ruleset_id: int):
        for rs in self.rulesetRepo:
            if int(rs.ruleSetID) == ruleset_id:
                self.rulesetRepo.remove(rs)
                
        self.save_ruleset_file()
        return rs

    def del_playlists_repo(self, playlist_id: int):
        for pl in self.playlistRepo:
            if int(pl.playlistID) == playlist_id:
                self.playlistRepo.remove(pl)
                
        self.save_playlist_file()
        return pl

    def del_users_repo(self, user_id: str):
        for user in self.userRepo:
            if int(user.userID) == user_id:
                self.userRepo.remove(user)
                
        self.save_user_file()
        return user
        
        
    # save files
    def save_tag_file(self):
        with open(self.tagFilename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.tagFieldnames)
            writer.writeheader()
            for tag in self.tagRepo:
                writer.writerow(asdict(tag))
    
    def save_song_file(self):
        with open(self.songFilename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.songFieldnames)
            writer.writeheader()
            for song in self.songRepo:
                writer.writerow(asdict(song))
                
    def save_rule_file(self):
        with open(self.ruleFilename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.ruleFieldnames)
            writer.writeheader()
            for rule in self.ruleRepo:
                writer.writerow(asdict(rule))
                
    def save_ruleset_file(self):
        with open(self.rulesetFilename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.rulesetFieldnames)
            writer.writeheader()
            for ruleset in self.rulesetRepo:
                writer.writerow(asdict(ruleset))
                
    def save_playlist_file(self):
        with open(self.playlistFilename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.playlistFieldnames)
            writer.writeheader()
            for playlist in self.playlistRepo:
                writer.writerow(asdict(playlist))
                
    def save_user_file(self):
        with open(self.userFilename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.userFieldnames)
            writer.writeheader()
            for user in self.userRepo:
                writer.writerow(asdict(user))


# Insantiate the DB
# -----------------

spotifyRepo = SpotifySQLModelRepo("sqlite:///spotify.db")
#   spotifyRepo = SpotifyCSVRepo("tags.csv", ["tagID", "name", "isNumeric"], "songs.csv", ["songID", "artist", "title", "album", "spotifyURI", "tags"], "rules.csv", ["ruleID", "tag", "requirement", "sort", "value", "count", "percent"], "rulesets.csv", ["ruleSetID", "name", "songCount", "ruleList"], "playlists.csv", ["playlistID", "name", "spotifyID", "generatedBy", "songList"], "users.csv", ["userID", "songLibrary", "playlistLibrary", "tagLibrary", "rulesetLibrary", "spotifyID"])

def add_dummy_data():
    for key,value in tags.items():
        spotifyRepo.new_tags_repo(value)
    for key,value in songs.items():
        spotifyRepo.new_songs_repo(value)
    for key,value in rules.items():
        spotifyRepo.new_rules_repo(value)
    for key,value in rulesets.items():
        spotifyRepo.new_rulesets_repo(value)
    for key,value in playlists.items():
        spotifyRepo.new_playlists_repo(value)
    for key,value in users.items():
        spotifyRepo.new_users_repo(value)

#   add_dummy_data()   # only run once if you have empty tables


# FASTAPI CRUD operators
# ----------------------

# the getters

@app.get("/")
async def root():
    return {"message":"Welcome to the Spotify Playlist Generator API"}
    
@app.get("/getters/tags/{tag_id}")
def read_tags(tag_id: int):
    try:
        return {"tag_id": tag_id, "tag": spotifyRepo.read_tags_repo(tag_id)}
    except:
        raise HTTPException(status_code=404, detail="tag not found")

@app.get("/getters/songs/{song_id}")
def read_songs(song_id: int):
    try:
        return {"song_id": song_id, "song": spotifyRepo.read_songs_repo(song_id)}
    except:
        raise HTTPException(status_code=404, detail="song not found")
    
@app.get("/getters/rules/{rule_id}")
def read_rules(rule_id: int):
    try:
        return {"rule_id": rule_id, "rule": spotifyRepo.read_rules_repo(rule_id)}
    except:
        raise HTTPException(status_code=404, detail="rule not found")
    
@app.get("/getters/rulesets/{ruleset_id}")
def read_rulesets(ruleset_id: int):
    try:
        return {"ruleset_id": ruleset_id, "ruleset": spotifyRepo.read_rulesets_repo(ruleset_id)}
    except:
        raise HTTPException(status_code=404, detail="ruleset not found")

@app.get("/getters/playlists/{playlist_id}")
def read_playlists(playlist_id: int):
    try:
        return {"playlist_id": playlist_id, "playlist": spotifyRepo.read_playlists_repo(playlist_id)}
    except:
        raise HTTPException(status_code=404, detail="playlist not found")

@app.get("/getters/users/{user_id}")
def read_users(user_id: str):
    try:
        return {"user_id": user_id, "user": spotifyRepo.read_users_repo(user_id)}
    except:
        raise HTTPException(status_code=404, detail="user not found")


# the setters

@app.post("/setters/tags/{tag_id}")
def new_tags(tag: Tag):
    try: 
        spotifyRepo.new_tags_repo(tag)
        return spotifyRepo.read_tags_repo(tag.tagID)
    except:
        raise HTTPException(status_code=400, detail="tag already exists")

@app.post("/setters/songs/{song_id}")
def new_songs(song: Song):
    try:
        spotifyRepo.new_songs_repo(song)
        return spotifyRepo.read_songs_repo(song.songID)
    except:
        raise HTTPException(status_code=400, detail="song already exists")

@app.post("/setters/rules/{rule_id}")
def new_rules(rule: Rule):
    try:
        spotifyRepo.new_rules_repo(rule)
        return spotifyRepo.read_rules_repo(rule.ruleID)
    except:
        raise HTTPException(status_code=400, detail="rule already exists")

@app.post("/setters/rulesets/{ruleset_id}")
def new_rulesets(ruleset: Ruleset):
    try:
        spotifyRepo.new_rulesets_repo(ruleset)
        return spotifyRepo.read_rulesets_repo(ruleset.ruleSetID)
    except:
        raise HTTPException(status_code=400, detail="ruleset already exists")

@app.post("/setters/playlists/{playlist_id}")
def new_playlists(playlist: Playlist):
    try:
        spotifyRepo.new_playlists_repo(playlist)
        return spotifyRepo.read_playlists_repo(playlist.playlistID)
    except:
        raise HTTPException(status_code=400, detail="playlist already exists")

@app.post("/setters/users/{user_id}")
def new_users(user: User):
    try:
        spotifyRepo.new_users_repo(user)
        return spotifyRepo.read_users_repo(user.userID)
    except:
        raise HTTPException(status_code=400, detail="user already exists")


# the fixers

@app.put("/fixers/tags/{tag_id}")
def mod_tags(tag_id: int, field: str, value):
    try:
        spotifyRepo.mod_tags_repo(tag_id, field, value)
        return spotifyRepo.read_tags_repo(tag_id)
    except:
        raise HTTPException(status_code=404, detail="tag not found")

@app.put("/fixers/songs/{song_id}")
def mod_songs(song_id: int, field: str, value):
    try:
        spotifyRepo.mod_songs_repo(song_id, field, value)
        return spotifyRepo.read_songs_repo(song_id)
    except:
        raise HTTPException(status_code=404, detail="song not found")

@app.put("/fixers/rules/{rule_id}")
def mod_rules(rule_id: int, field: str, value):
    try:
        spotifyRepo.mod_rules_repo(rule_id, field, value)
        return spotifyRepo.read_rules_repo(rule_id)
    except:
        raise HTTPException(status_code=404, detail="rule not found")

@app.put("/fixers/rulesets/{ruleset_id}")
def mod_rulesets(ruleset_id: int, field: str, value):
    try:
        spotifyRepo.mod_rulesets_repo(ruleset_id, field, value)
        return spotifyRepo.read_rulesets_repo(ruleset_id)
    except:
        raise HTTPException(status_code=404, detail="ruleset not found")

@app.put("/fixers/playlists/{playlist_id}")
def mod_playlists(playlist_id: int, field: str, value):
    try:
        spotifyRepo.mod_playlists_repo(playlist_id, field, value)
        return spotifyRepo.read_playlists_repo(playlist_id)
    except:
        raise HTTPException(status_code=404, detail="playlist not found")

@app.put("/fixers/users/{user_id}")
def mod_users(user_id: str, field: str, value):
    try:
        spotifyRepo.mod_users_repo(user_id, field, value)
        return spotifyRepo.read_users_repo(user_id)
    except:
        raise HTTPException(status_code=404, detail="user not found")


# the wipers

@app.delete("/wipers/tags/{tag_id}")
def del_tags(tag_id: int):
    try:
        tag = spotifyRepo.read_tags_repo(tag_id)
        spotifyRepo.del_tags_repo(tag_id)
        return tag
    except:
        raise HTTPException(status_code=404, detail="tag not found")

@app.delete("/wipers/songs/{song_id}")
def del_songs(song_id: int):
    try:
        song = spotifyRepo.read_songs_repo(song_id)
        spotifyRepo.del_songs_repo(song_id)
        return song
    except:
        raise HTTPException(status_code=404, detail="song not found")

@app.delete("/wipers/rules/{rule_id}")
def del_rules(rule_id: int):
    try:
        rule = spotifyRepo.read_rules_repo(rule_id)
        spotifyRepo.del_rules_repo(rule_id)
        return rule
    except:
        raise HTTPException(status_code=404, detail="rule not found")

@app.delete("/wipers/rulesets/{ruleset_id}")
def del_rulesets(ruleset_id: int):
    try:
        rs = spotifyRepo.read_rulesets_repo(ruleset_id)
        spotifyRepo.del_rulesets_repo(ruleset_id)
        return rs
    except:
        raise HTTPException(status_code=404, detail="ruleset not found")

@app.delete("/wipers/playlists/{playlist_id}")
def del_playlists(playlist_id: int):
    try:
        pl = spotifyRepo.read_playlists_repo(playlist_id)
        spotifyRepo.del_playlists_repo(playlist_id)
        return pl
    except:
        raise HTTPException(status_code=404, detail="playlist not found")

@app.delete("/wipers/users/{user_id}")
def del_users(user_id: str):
    try:
        user = spotifyRepo.read_users_repo(user_id)
        spotifyRepo.del_users_repo(user_id)
        return user
    except:
        raise HTTPException(status_code=404, detail="user not found")


# if you want to use uvicorn

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)