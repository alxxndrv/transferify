import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read user-library-modify"
cache_path = ".spotify_oauth"


def generate_auth_url():
    auth_manager = SpotifyOAuth(scope=scope, cache_path=cache_path)
    url = auth_manager.get_authorize_url()
    return auth_manager, url


def create_spotify(auth_manager, url):
    code = auth_manager.parse_response_code(url)
    token_info = auth_manager.get_access_token(code)
    access_token = token_info['access_token']
    spotify = spotipy.Spotify(access_token)
    return spotify


def get_name(spotify):
    return spotify.current_user().get('display_name')
