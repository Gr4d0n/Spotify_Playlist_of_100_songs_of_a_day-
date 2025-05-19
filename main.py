import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import pprint
from tsotd import SongList

# Accessing the credentials
load_dotenv()
spotify_client_id = os.environ["SPOTIFY_CLIENT_ID"]
spotify_secret = os.environ["SPOTIFY_CLIENT_SECRET"]
redirect_uri = os.environ["REDIRECT_URI"]

# For authorization of the application with the spotify
authentication = SpotifyOAuth(
    client_id=spotify_client_id,
    client_secret=spotify_secret,
    redirect_uri=redirect_uri,
    scope="playlist-read-private playlist-modify-public playlist-modify-private",
    show_dialog=True,
    cache_path=".cache",
    username='---------'
)

# For creating the list
create_list = SongList()
create_list.create_TSOTD()

# Creating spotipy instance
sp = spotipy.Spotify(auth_manager=authentication)

# Creating URIs
list_of_songs = []
uri_list = []
date = create_list.date
with open(f"top_songs_{date}.txt", "r") as file:
    for i in file.read().splitlines():
        list_of_songs.append(i.split('. ')[1])

for i in list_of_songs:

    try:
        song_uri = sp.search(i, type='track', limit=1)['tracks']['items'][0]['uri']
    except IndexError:
        continue
    else:
        uri_list.append(song_uri)

# Creating playlist
create_playlist = sp.user_playlist_create(
    user=sp.current_user()['id'],
    name=f"Billboard_top_100_date_{date}",
    public=True,
    description='Top Song of The Above Date'
)

# Adding songs to the playlist
sp.playlist_add_items(create_playlist['id'], uri_list)
