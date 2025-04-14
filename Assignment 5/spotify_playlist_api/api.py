from django.shortcuts import get_object_or_404

from ninja import NinjaAPI, Schema, Router, Field
from jobs.api import router as alt_router

from job.models import Song
from job.models import Playlist

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

class PlaylistIn(Schema):
    name: str
    spotifyID: str
    generatedBy: int = None
    songList: int = None

class PlaylistOut(Schema):
    playlistID: int
    name: str
    spotifyID: str
    generatedBy: int = None
    songList: int = None

#------ API SETUP

api = NinjaAPI()

# SONG

@api.post("/song")
def create_song(request, song: SongIn):
    # worker_info = song.dict()
    # worker = Song(**worker_info)
    # song = Song.objects.create(worker)
    Song.objects.create(**song.dict())
    return song

@api.get("/song/{song_id}", response=SongOut)
def get_song(request, song_id: int):
    song = get_object_or_404(Song, id=song_id)
    return song

@api.get("/song", response=list[SongOut])
def list_songs(request):
    songs = Song.objects.all()
    return songs

@api.put("/song/{song_id}")
def update_song(request, song_id: int, payload: SongIn):
    song = get_object_or_404(Song, id=song_id)
    for attr, value in payload.dict().items():
        setattr(song, attr, value)
    song.save()
    return {"success": True, "song": song}

@api.delete("/song/{song_id}")
def delete_song(request, song_id: int):
    song = get_object_or_404(Song, id=song_id)
    song.delete()
    return {"success": True, "song": song}

# PLAYLIST

@api.post("/playlist")
def create_playlist(request, playlist: PlaylistIn):
    Playlist.objects.create(**playlist.dict())
    return playlist

@api.get("/playlist/{playlist_id}", response=PlaylistOut)
def get_playlist(request, playlist_id: int):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    return playlist

@api.get("/playlist", response=list[PlaylistOut])
def list_playlists(request):
    playlists = Playlist.objects.all()
    return playlists

@api.put("/playlist/{playlist_id}")
def update_playlist(request, playlist_id: int, payload: PlaylistIn):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    for attr, value in payload.dict().items():
        setattr(playlist, attr, value)
    playlist.save()
    return {"success": True, "playlist": playlist}

@api.delete("/playlist/{playlist_id}")
def delete_playlist(request, playlist_id: int):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    playlist.delete()
    return {"success": True, "playlist": playlist}
    
api.add_router("/import/", alt_router)