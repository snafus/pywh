from flask import Flask, redirect, session
from authlib.integrations.flask_client import OAuth
from authlib.jose import jwt
import json
from flask import url_for, render_template
import os

# Based on the official Authlib example for Google:
# https://github.com/authlib/demo-oauth-client/blob/master/flask-google-login/app.py

app = Flask(__name__)
app.config.from_pyfile("app.cfg")

CONF_URL = 'https://auth.cern.ch/auth/realms/cern/.well-known/openid-configuration'
LOGOUT_URL = 'https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/logout'

oauth = OAuth()
oauth.register(
    'sso',
    server_metadata_url=CONF_URL,
    client_kwargs={'scope': 'openid oidc-cern-login-info'}
)
oauth.init_app(app)

@app.route('/')
def homepage():
    user = session.get('user')
    return render_template('home.html', user=user)

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.sso.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = oauth.sso.authorize_access_token()
    user = oauth.sso.parse_id_token(token)
    # Use the user object for authorization (e.g. check user roles)
    session['user'] = user
    return redirect(url_for('homepage'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect("{}?redirect_uri={}".format(
        LOGOUT_URL,
        url_for('homepage', _external=True))
    )

app.secret_key = os.urandom(24)
app.run(port=8080)

