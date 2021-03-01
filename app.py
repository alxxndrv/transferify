from flask import Flask, render_template
from spotify_backend import generate_auth_url

app = Flask(__name__)

spotify_storage = {}


@app.route('/')
def index():
    return render_template('index.html', url=generate_auth_url()[1])


if __name__ == '__main__':
    app.run()
