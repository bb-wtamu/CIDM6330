# Assignment 1
## Front Page
**Spotify Playlist Generator**  
**Brandon Baither**  
CIDM 6330  
02/12/2025

## Introduction
This system is to allow a Spotify customer the ability to create what is functionally an external database of their songs. This database can allow for tagging/rating of songs through either manual app input or through spotify playlists, with the end-goal of allowing for custom playlist generation through a set of user-defined rules. This will all be accomplished via interactions with the free Spotify web API.

## Table of Contents
	
1. Front matter
    1. Front page
    2. Introduction
    3. Table of contents
2. Requirements statements
    1. User Stories
	2. Use Cases
	3. Features
	4. Gherkin Validation
3. Specifications
    1. Concept
    2. UX Notes
    3. Interfaces (Controls)
    4. Behaviors

## User Stories
| Story                                                                     | Priority |
| ------------------------------------------------------------------------- | -------- |
| Users can login to their Spotify account                                  | High     |
| Users can import playlists from their spotify account                     | High     |
| Users can assign ratings or tags to all the songs in an imported playlist | Med      |
| Users can manually assign ratings or tags to songs                        | Low      |
| Users can generate playlists from the app in their spotify account        | High     |
| Users can define rules to guide the generation of playlists               | Med      |
| Users can perform actions on existing playlists in their account          | Low      |

## Use Cases
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
4. Manually edit song database
	* TBD
5. Edit existing playlists
	* TBD

## Features
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

## Gherkin Validation
I've never used gherkin specifically, but this would seem to be a definition of a (automated?) test suite for validating this entire program? That would probably be hundreds of tests, so I'm just going to try and jot down a few examples based on a quick google of gherkin syntax for now.
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

## Specification Concept
This system is conceptualized as a basic GUI, with hopefully only one or two layers below the primary menu. On startup, the user will login to their spotify account. They will then be presented with the list of things the program can do. Selecting any of these will take the user one level down where the appropriate options will be presented to them. Some of these layers might potentially allow the user to view a third layer showing playlists or songs. Upon completing their inputs the system will take the appropriate action and return the user to the base menu.  

Data storage for songs will be based on the unique spotify URI assigned to each song. If a song is imported that does not exist it will get a new entry with details - probably Spotify URI, Artist, Title, Album, and any user defined ratings/tags applied. If a song is imported that already exists in the song database then the tags/ratings set by the new import will be applied to the existing entry. Conflicts (say it already has a rating of 4 and user says to set rating to 5) will probably just overwite, but potential to ask exists.

## UX Notes
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
	
## Interfaces
* The main external interface is obviously Spotify, which has a free web API as specified at [Spotify Web API](https://developer.spotify.com/documentation/web-api).
    * Need to be able to login/validate user credentials - spotify handles this.
	* Need to be able to import playlists.
	* Need to be able to save new playlists.
	* Need to be able to modify existing playlists
	* One concern is how the api allows for interacting with "local" songs - ie purchased aac/mp3 files the user has added to spotify. Uncertain what is possible there.
* Depending on how the song database is managed this could also be an external interface of sorts, but at least at first this will probably just utilize internal python data structures.

## Behaviors
![Activity Diagram for Logging in to Spotify.](/activity_diagram_login_spotify.png "Login to Spotify Activity Diagram")
