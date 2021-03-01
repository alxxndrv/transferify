from flask import Flask, render_template, request, make_response, redirect
from spotify_backend import generate_auth_url, create_spotify
from uuid import uuid4
import spotipy

app = Flask(__name__)

# Сохраняем объекты Spotify
spotify_storage = {}
# Сохраняем все auth managers для того, чтобы создавать объект Spotify
auth_managers = {}


def generate_session_id():
    return str(uuid4())


@app.route('/')
def index():
    auth_manager, url = generate_auth_url()
    session_id = generate_session_id()
    auth_managers[session_id] = auth_manager
    response = make_response(render_template('index.html', url=url))
    user_id = request.cookies.get('userID')
    if not user_id:  # Проверяем, есть ли в куках userID
        user_id = generate_session_id()
        response.set_cookie('userID', user_id)

    if not auth_managers.get(user_id):
        auth_managers[user_id] = auth_manager

    return response


@app.route('/transfer')
def transfer_page():
    return 'transfer_page'


@app.route('/oauth')
def oauth():
    # TODO: проверка, есть ли user_id в auth и в spotify
    user_id = request.cookies.get('userID')
    auth_manager = auth_managers.get(user_id)  # Достаем auth manager из словаря
    if not auth_manager:
        response = make_response(redirect('/'))
        response.set_cookie('userID', '', expires=0)
        return response
    auth_manager.parse_auth_response_url(request.url)  # Парсим урл оауфа
    spotify_storage[user_id] = create_spotify(auth_manager)
    return redirect('transfer')


if __name__ == '__main__':
    app.run()
