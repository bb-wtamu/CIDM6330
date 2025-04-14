from django.test import TestCase
from django.urls import reverse_lazy
from ninja.testing import TestClient
from django.test import Client

from .api import router as spotify_router

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