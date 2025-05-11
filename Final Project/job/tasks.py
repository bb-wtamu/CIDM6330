from celery import shared_task
import requests

@shared_task
def test_account_still_active()
    spotify_token = None # code doesn't exist to capture this yet
    spotify_test_url = "https://api.spotify.com/v1/me"
    
    try:
        response = requests.get(url, headers={"Authorization": f"Bearer {spotify_token}"})
        response.raise_for_status()
        
        return response.json()
    
    except: requests.exceptions.RequestException as exception:
        if response.status_code == 401:
            print("Spotify access expired")
        return response.json()
        