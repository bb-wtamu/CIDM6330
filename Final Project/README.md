# Final Project
**Spotify Playlist Generator**  
**Brandon Baither**  
CIDM 6330  
05/10/2025

My project is a playlist generation tool for [Spotify](https://open.spotify.com). While the service does a pretty incredible job of generating playlists of songs you like or that it thinks you will like, it has very few tools to assist in the on-the-fly generation of such for yourself, assuming you would like any control over that process. This was intended to be a tool that could step into that gap. I won't say I reached that goal - there is no actual integration for spotify in my app, and it doesn't actually do much of what it promises - but the beginnings of an API for accomplishing that goal are in place.

## Design Documentation
### Ubiquitous Language Glossary
The provided link for this topic didn't work, but googling suggests this is simply a glossary of common terminology to the system.

* Associate: The process of identifying what objects belong to a particular user; they are "associated" to them.
* Playlist: An ordered collection of songs.
* Rule: A definition by which songs are selected to be added to a playlist. This is essentially a filter to apply to a complete list of songs to pull a small group of them out, possible via both eliminating some options and using various selection criteria to pick a certain number from those left. An example would be selecting 50 songs randomly from all of the 4 or 5 rated Rock songs in the library. This rule elminates all songs with genres other than rock and all songs with ratings below 4. From those left, it selects 50 via a random process.
* Ruleset: A collection of rules by which all the songs for a particular playlist are selected. This can be made up of just one rule, or a collection of many rules each adding a selection of songs to the whole list.
* SpotifyID/SpotifyURI: The URI used by spotify to identify a particular user's account, a particular song, or a particular playlist.
* Spotify Token: The access token provided to us that allows us to manipulate a user's spotify account. It can be revoked or time out, at which point a new token will be required before the system can interact with spotify on a user's behalf.
* Tag: the definition of a piece of extraneous information about a song. For example, "Genre" would be a tag, while something like "Rock" or "R&B" would be the value of that tag when assigned to a particular song. Or "Rating" would be a tag, with values between 1 and 5.

### User Stories
| Story                                                                     | Priority |
| ------------------------------------------------------------------------- | -------- |
| Users can login to their Spotify account                                  | High     |
| Users can import playlists from their spotify account                     | High     |
| Users can assign ratings or tags to all the songs in an imported playlist | Med      |
| Users can manually assign ratings or tags to songs                        | Low      |
| Users can generate playlists from the app in their spotify account        | High     |
| Users can define rules to guide the generation of playlists               | Med      |
| Users can perform actions on existing playlists in their account          | Low      |

### Use Cases
1. Login to Account
	* User indicates desire to login to Spotify account
	* System redirect user to Spotify credential sharing web page
	* User logs in to Spotify if necessary
	* User accepts prompt to provide system access to their Spotify account
	* System presents user with the logged in view showing their account details
2. Import Playlist
	* User indicates desire to import a playlist
	* System presents user a list of their Spotify playlists
	* User selects the playlist(s) from their spotify account to import
	* System presents user with the import options
	* User inputs rating / tags to apply to the songs
	* User selects whether the playlist should be imported as a playlist as well, or just the songs indexed (maybe unneeded)
	* System imports the playlist into the song database as directed and returns to standard view
3. Generate Playlist
	* User indicates desire to generate a new playlist
	* System presents user with rule generation page
	* User inputs a name for the new playlist
	* User defines the rules by which the new playlist should be generated
	* System warns user if their rules don't make perfect sense (ie percentages add up to 60 instead of 100) allowing them option to correct or for them to be automagically normalized
	* User proceeds until satisfied with rules
	* System generates new playlist and returns user to standard view

### Features
* Login user to Spotify account
* Import user's playlist list from spotify
* Import the contents of a playlist from spotify
* Save a playlist to user's spotify account
* Store playlists in appropriate data structures
* Store song list in approprate data structure
* Store ratings/tags with the songs in appropriate data structure
* Present main menu of options for what to do to user
* Allow user to define playlist to be imported and define tags/rating to be applied to songs
* Allow user to define rules for generating a new playlist
* Validate rules for playlist generation
* Normalize invalid rules for playlist generation
* Generate a new playlist according to rules

### Gherkin Validation
1. 
```
Feature: Generate a new playlist according to rules
		
Scenario: Legitimate request based on ratings
	Given a song database has been imported
	And the songs all have ratings assigned
	When the user requests a randomized playlist of 200 songs all with ratings of 5
	Then the system generates a playlist of 200 songs
	And the songs in it are selected randomly
	And the songs in it all have ratings of 5
```
	
2.
```
Feature: Login user to Spotify account / Import user's playlist list from Spotify
	
Scenario: Valid login to Spotify
	Given the user has a spotify account
	When the user logs in correctly
	Then the system displays the users Spotify account name
	And the system presents the user a list of their playlists
```
			
3.
```
Feature: Validate rules for playlist generation
	
Scenario: Invalid rules input
	Given a song database has been imported
	And the songs have ratings spread between 1-5
	When the user makes a request for a new playlist consisting of 60% 5-rated songs and 30% 4-rated songs
	Then the system informs the user their percentages add up to 90, not 100, and asks whether they wish to correct or have the system normalize
			
Scenario: Valid rules input
	Given a song database has been imported
	And the songs have ratings spread between 1-5
	When the user makes a request for a new playlist consisting of 60% 5-rated songs and 40% 4-rated songs
	The system informs the user their rules are valid and generates a new playlist
```

### Specification Concept
This system is conceptualized as a basic GUI, with hopefully only one or two layers below the primary menu. On startup, the user will login to their spotify account. They will then be presented with the list of things the program can do. Selecting any of these will take the user one level down where the appropriate options will be presented to them. Some of these layers might potentially allow the user to view a third layer showing playlists or songs. Upon completing their inputs the system will take the appropriate action and return the user to the base menu.  

Data storage for songs will be based on the unique spotify URI assigned to each song. If a song is imported that does not exist it will get a new entry with details - probably Spotify URI, Artist, Title, Album, and any user defined ratings/tags applied. If a song is imported that already exists in the song database then the tags/ratings set by the new import will be applied to the existing entry. Conflicts (say it already has a rating of 4 and user says to set rating to 5) will probably just overwite, but potential to ask exists.

### UX Notes
* On loading sytem: present base menu grayed out to show the user what the program is capable of, but have the only selectable item be to login to spotify. Selecting this will take the user to an external spotify web page for logging in and accepting the permissions the program requires. They will then be returned to the software.
* General logged in basic menu will potentially show a scrollable list of the user's existing playlists, as well as the following options:
    * Import playlist to song database
	* Generate new playlist
	* View/edit song database
	* Modify existing playlist
* Import playlist panel will present a list of playlists to choose from. After choosing more option will appear for setting ratings/tags to the songs imported. Specifics on tagging options still needs to be developed, but the idea is things like setting a genre or mood or BPM or really any way of categorizing music that the user might come up with. These are then the major inputs used later for generating playlist rules. Then of course an "Import" button once everything is configured to the user's desires. Afterwards the user will be returned to the main menu.
* Generate new playlist panel will have a flexible system for defining rules. Design still undetermined, but the idea would be to select a number of tracks to put in the playlist, set some basic ideas such as "shuffle/randomize", and then define where the songs should be pulled from using tags/ratings. For example, setup a shuffled playlist of 500 songs, 20% of which should be tagged as "rock" with a rating of 5, 50% tagged as "pop" with a rating of 5, and 30% as "pop" or "rock" and a rating of 4.
* View/edit song database would need the ability to display and, perhaps more importantly, filter the song database. General use case would be to go in and find any songs that don't have a rating or a genre tag, etc and add those. Potentially a search for songs that duplicate both "Artist" and "Song Title" to check for if you've got the same song in there multiple times with different albums or something?
* Modify existing playlist would have the ability to select an existing playlist and then apply a function to it from a list. Shuffling or sorting based on various factors are the obvious options, not sure what else might make sense.
	
### Interfaces
* The main external interface is obviously Spotify, which has a free web API as specified at [Spotify Web API](https://developer.spotify.com/documentation/web-api).
    * Need to be able to login/validate user credentials - spotify handles this.
	* Need to be able to import playlists.
	* Need to be able to save new playlists.
	* Need to be able to modify existing playlists
	* One concern is how the api allows for interacting with "local" songs - ie purchased aac/mp3 files the user has added to spotify. Uncertain what is possible there.
* Depending on how the song database is managed this could also be an external interface of sorts, but at least at first this will probably just utilize internal python data structures.

### Behaviors
Activity Diagram: Logging in to Spotify  

![Activity Diagram for Logging in to Spotify.](/Final%20Project/activity_diagram_login_spotify.png "Login to Spotify Activity Diagram")

Activity Diagram: Generating a New Playlist  

![Activity Diagram for Generating a New Playlist.](/Final%20Project/activity_diagram_new_playlist.png "Generating a New Playlist")

### Entity Relationship Diagram

![ERD for the Spotify Playlist Generator](/Final%20Project/ERD-light.png "ERD for the Spotify Playlist Generator")

## The API
The API created for this project is written using Django Ninja.

### The Models
Models were created for all of the tables needed in my data schema, with the exception of the association tables between the User class and its libraries - these are generated automatically using Django's ManyToManyFields. The full code for this can be found within the /job/models.py file.

```python
class Song(models.Model):
    songID = models.AutoField(primary_key=True)
    artist = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    spotifyURI = models.CharField(max_length=200)
    
class Tag(models.Model):
    tagID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    isNumeric = models.booleanField()
    
class Tagged(models.Model):
    taggedID = models.AutoField(primary_key=True)
    song = models.ForeignKey(Song, models.CASCADE)
    tag = models.ForeignKey(Tag, models.CASCADE)
    value = models.CharField(max_length=70, null=True)
    value_num = models.IntegerField(null=True)
    
class Ruleset(models.Model):
    rulesetID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    songCount = models.IntegerField(null=True)
    
class Rule(models.Model):
    ARTIST = 1
    TITLE = 2
    ALBUM = 3
    SHUFFLE = 4
    SORT_STRATEGY_CHOICES = {
        ARTIST: "Artist",
        TITLE: "Title",
        ALBUM: "Album",
        SHUFFLE: "Shuffle",
    }
    
    CONTAINS = 1
    NOT_CONTAINS = 2
    GREATER = 3
    LESS = 4
    EQUALS = 5
    REQUIREMENT_CHOICES = {
        CONTAINS = "Contains",
        NOT_CONTAINS = "Does Not Contain",
        GREATER = "Greater Than",
        LESS = "Less Than",
        EQUALS = "Equal To",
    }
    
    ruleID = models.AutoField(primary_key=True)
    tag = models.ForeignKey(Tag, models.CASCADE)
    ruleset = models.ForeignKey(Ruleset, models.CASCADE)
    requirement = models.IntegerField(choices=REQUIREMENT_CHOICES)
    sort_strategy = models.IntegerField(choices=SORT_STRATEGY_CHOICES)
    threshold = models.IntegerField(null=True)
    value = models.CharField(max_length=70, null=True)
    count = models.IntegerField()
    percent = models.DecimalField(max_digits=4, decimal_places=2)

class Playlist(models.Model):
    playlistID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    spotifyID = models.CharField(max_length=200)
    generatedBy = models.ForeignKey(Ruleset, models.SET_NULL, null=True)
    
class PlaylistAssignment(models.Model):
    playlistAssignmentID = models.AutoField(primary_key=True)
    song = models.ForeignKey(Song, models.CASCADE)
    playlist = models.ForeignKey(Playlist, models.CASCADE)
    position = models.IntegerField()
    
class User(models.Model):
    userID = models.AutoField(primary_key=True)
    spotifyID = models.CharField(max_length=200)
    songLibrary = models.ManyToManyField(Song)
    playlistLibrary = models.ManyToManyField(Playlist)
    tagLibrary = models.ManyToManyField(Tag)
    rulesetLibrary = models.ManyToManyField(Ruleset)
```

### CRUD Operations
Basic CRUD operators were created for every model used by the system. These can be found in full in the /spotify_playlist_api/api.py file. Presented here is a single example.

```python
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
```

### Beyond CRUD
Some more complicated functions were added to the API, to enable functionality that will be necessary in the completed tool. These can also be found in the /spotify_playlist_api/api.py file.

```python
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
```

### Event-Driven Architecture
The system includes an event-driven system utilizing celery with the django_celery_beat scheduler. A test task was created which would be used to verify the user's spotify API access is still valid. This would be scheduled from the django admin interface as desired, likely periodically - say every 15 minutes. This is defined in full in the job/tasks.py and spotify_playlist_api/settings.py files.

```python
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
```

### Unit Tests
Several unit tests were developed using Django's unit testing utilities. These can be viewed in full in the job/tests.py file.

```python
class TestSongGet(TestCase)
    def setUp(self):
        self.client = TestClient(api)
        
        self.testSong = Song.objects.create(artist = "TestArtist", fitle = "TestTitle", album = "TestAlbum", spotifyURI = "TestURI")
        
    def test_get_song(self):
        response = self.client.get(f"/song/{self.testSong.songID}")
        expected = { "songID": self.testSong.songID, "artist": "TestArtist", "title": "TestTitle", "album": "TestAlbum", "spotifyURI": "TestURI" }
                
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)
```
