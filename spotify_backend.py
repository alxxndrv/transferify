import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read user-library-modify"


def generate_auth_url():
    auth_manager = SpotifyOAuth(scope=scope)
    url = auth_manager.get_authorize_url()
    return auth_manager, url


def create_spotify(auth_manager):
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify
