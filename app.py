from flask import Flask, render_template, request
from spotify_backend import generate_auth_url

app = Flask(__name__)

# Сохраняем объекты Spotify
spotify_storage = {}
# Сохраняем все auth managers для того, чтобы создавать объект Spotify
auth_managers = {}


@app.route('/')
def index():
    return render_template('index.html', url=generate_auth_url()[1])


@app.route('/oauth')
def oauth():
    # TODO: oauth
    pass


if __name__ == '__main__':
    app.run()
