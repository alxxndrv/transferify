from flask import Flask, render_template, request, make_response, redirect
from spotify_backend import generate_auth_url, create_spotify, get_name
from uuid import uuid4
from pymongo import MongoClient
from vk_backend import parse_songs, get_id

app = Flask(__name__)
client = MongoClient()

# Сохраняем объекты Spotify
spotify_storage = {}
# Сохраняем все auth managers для того, чтобы создавать объект Spotify
auth_managers = {}
# База данных с query и errors
db = client.transferify


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


@app.route('/transfer', methods=['GET', 'POST'])  # Через GET — отображаем страницу
def transfer_page():
    user_id = request.cookies.get('userID')
    spotify = spotify_storage.get(user_id)
    if not spotify:
        return redirect('/')  # Возвращаем юзера на главную страницу, если он перешел на трансфер просто так (без
        # авторизации)
    user_name = get_name(spotify)
    if request.method == 'GET':  # Если GET... (перебрасываем на страницу ввода short name)
        return render_template('transfer.html', name=user_name)
    # Если POST... (обрабатываем треки)
    short_name = request.form['short_name']  # Получаем short name, которое ввел пользователь
    vk_id = get_id(short_name)  # Получаем vk_id для парсинга песен

    user_data = {
        'user_id': user_id,
        'short_name': short_name,
        'vk_id': vk_id,
        'query': [],  # Выгружаемые песни
        'errors': []  # Ошибки в экспорте (выводятся на экране после экспорта)
    }

    user_data['query'] = parse_songs(user_data['vk_id'])  # Парсим песни, todo: multiprocessing
    db.sessions.insert_one(user_data)
    return redirect('/transfer/confirm')


@app.route('/transfer/confirm')
def transfer_confirmation():
    return ''  # todo: transfer confirmation


@app.route('/oauth')
def oauth():
    user_id = request.cookies.get('userID')
    auth_manager = auth_managers.get(user_id)  # Достаем auth manager из словаря
    if not auth_manager:  # Если user_id нет в auth_managers, то
        response = make_response(redirect('/'))
        response.set_cookie('userID', '', expires=0)  # Удаляем user_id из кук и перебрасыаем на стартовую страницу
        return response
    spotify_storage[user_id] = create_spotify(auth_manager, request.url)
    return redirect('transfer')


if __name__ == '__main__':
    app.run()
