from celery import shared_task
import requests

@shared_task
def import_playlist(user: str, playlist: str):
    print("importa a playlist from spotify")
    
def test_account_still_active(user: str)
    print("test that the account is still logged in to spotify")