from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "spotify_playlist_api.settings"
)  # necessary to set the settings module for Django
# This will make sure the app is always imported when Django starts so that shared_task will use this app.
# This is important for the task to be registered with the Django app.


app = Celery("spotify_playlist_api")  # project name
app.conf.enable_utc = False

app.config_from_object(settings, namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


app.conf.CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

app.conf.beat_schedule = {
    "test_account_crontab": {
        "task": "job.tasks.test_account_still_activee",
        "schedule": crontab(minute="*/15"),
        "args": ("username",),
    },
}
