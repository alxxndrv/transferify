import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read user-library-modify"


def generate_auth_url():
    auth_manager = SpotifyOAuth(scope=scope)
    url = auth_manager.get_authorize_url()
    return auth_manager, url
