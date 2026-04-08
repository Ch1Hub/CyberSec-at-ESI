from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'REDACTED_FLASK_SESSION_SECRET'

oauth = OAuth(app)

# 🛠️ EXERCISE: COMPLETE THE CONFIGURATION BELOW
# Get these values from your Keycloak Client settings  
CONF_URL = "http://localhost:8080/realms/ESI-Corporate/.well-known/openid-configuration"
CLIENT_ID = "internal-webapp"
CLIENT_SECRET = "REDACTED_KEYCLOAK_CLIENT_SECRET"

oauth.register(
    name='keycloak',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    client_kwargs={'scope': 'openid profile email'}
)

@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.keycloak.authorize_redirect(redirect_uri)

@app.route('/auth')
def auth():
    token = oauth.keycloak.authorize_access_token()
    # 🛠️ EXERCISE: Verify the user and extract the 'department' claim
    user_info = token.get('userinfo')
    session['user'] = user_info
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
