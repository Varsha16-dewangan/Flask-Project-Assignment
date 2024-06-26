from flask import Flask, redirect, url_for, session, request, jsonify, render_template, flash
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session management

# Google OAuth2 configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# GitHub OAuth2 configuration
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
GITHUB_AUTHORIZATION_BASE_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Here you would typically check the credentials against your database
    # For this example, we'll use a hardcoded user
    if username == "example@email.com" and password == "password":
        session['user'] = username
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('home'))

@app.route("/dashboard")
def dashboard():
    if 'user' in session:
        return f"Welcome to your dashboard, {session['user']}!"
    return redirect(url_for('home'))

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# Google OAuth2 routes
@app.route("/login/google")
def login_google():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    oauth2_session = OAuth2Session(
        client_id=GOOGLE_CLIENT_ID,
        redirect_uri=url_for('callback_google', _external=True),
        scope=["openid", "email", "profile"]
    )

    authorization_url, state = oauth2_session.authorization_url(authorization_endpoint)
    session['oauth_state'] = state  # Store the OAuth state in session for security

    return redirect(authorization_url)

@app.route("/callback/google")
def callback_google():
    # Verify OAuth state to prevent CSRF attacks
    if request.args.get('state') != session.get('oauth_state'):
        return "Authorization failed: State mismatch"

    # Obtain authorization code from Google
    code = request.args.get('code')
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    oauth2_session = OAuth2Session(
        client_id=GOOGLE_CLIENT_ID,
        redirect_uri=url_for('callback_google', _external=True),
        state=session['oauth_state']
    )

    token = oauth2_session.fetch_token(
        token_url=token_endpoint,
        client_secret=GOOGLE_CLIENT_SECRET,
        code=code
    )

    # Fetch user information using the token
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    userinfo_response = oauth2_session.get(userinfo_endpoint)
    userinfo = userinfo_response.json()

    # Store user information in session (you can use it as needed)
    session['profile'] = userinfo

    return jsonify(userinfo)

# GitHub OAuth2 routes
@app.route("/login/github")
def login_github():
    github = OAuth2Session(GITHUB_CLIENT_ID)
    authorization_url, state = github.authorization_url(GITHUB_AUTHORIZATION_BASE_URL)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route("/callback/github")
def callback_github():
    github = OAuth2Session(GITHUB_CLIENT_ID, state=session['oauth_state'])
    token = github.fetch_token(GITHUB_TOKEN_URL, client_secret=GITHUB_CLIENT_SECRET,
                               authorization_response=request.url)
    session['oauth_token'] = token
    return redirect(url_for('profile_github'))

@app.route("/profile/github")
def profile_github():
    github = OAuth2Session(GITHUB_CLIENT_ID, token=session['oauth_token'])
    return jsonify(github.get('https://api.github.com/user').json())

if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.run(debug=True, port=8001)
