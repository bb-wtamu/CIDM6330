from django.test import TestCase
from django.urls import reverse_lazy, reverse
from ninja.testing import TestClient
from django.test import Client
from typing import List

from .api import router as spotify_router
from spotify_playlist_api.api import api
from .models import Song

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_index(self):
        path = reverse_lazy("apilist:index")
        response = self.client.get(path)
        assert response.status_code == 200, "API is not reachable"
        assert response.json() == {
            "message": "Spotify Playlist API"
        }, "Unexpected response message"
        
        
class TestSongGet(TestCase)
    def setUp(self):
        self.client = TestClient(api)
        
        self.testSong = Song.objects.create(artist = "TestArtist", fitle = "TestTitle", album = "TestAlbum", spotifyURI = "TestURI")
        
    def test_get_song(self):
        response = self.client.get(f"/song/{self.testSong.songID}")
        expected = { "songID": self.testSong.songID, "artist": "TestArtist", "title": "TestTitle", "album": "TestAlbum", "spotifyURI": "TestURI" }
                
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)
        
        
class TestSongList(TestCase)
    def setUp(self):
        self.client = TestClient(api)
        
        self.testSong1 = Song.objects.create(artist = "TestArtist1", fitle = "TestTitle1", album = "TestAlbum1", spotifyURI = "TestURI1")
        self.testSong2 = Song.objects.create(artist = "TestArtist2", fitle = "TestTitle2", album = "TestAlbum2", spotifyURI = "TestURI2")
        
    def test_list_songs(self):
        response = self.client.get("/song")
        expected = [
            { "songID": self.testSong1.songID, "artist": "TestArtist1", "title": "TestTitle1", "album": "TestAlbum1", "spotifyURI": "TestURI1" },
            { "songID": self.testSong2.songID, "artist": "TestArtist2", "title": "TestTitle2", "album": "TestAlbum2", "spotifyURI": "TestURI2" }
        ]            
                
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)