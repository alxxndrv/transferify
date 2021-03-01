from flask import Flask, render_template, Request
from spotify_backend import generate_auth_url

app = Flask(__name__)

spotify_storage = {}
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
