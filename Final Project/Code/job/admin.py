from django.contrib import admin

from .models import Playlist

# Register your models here.
@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("name", "spotifyID")
    # list_filter = ("department")
    search_fields = ("name", "spotifyID")
    ordering = ("name", "spotifyID")