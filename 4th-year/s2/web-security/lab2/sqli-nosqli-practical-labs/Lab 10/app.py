import time
import os
import pymysql
from flask import Flask, request, render_template, make_response

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASS', 'root'),
    'database': os.environ.get('DB_NAME', 'lab10'),
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    retries = 30
    while retries > 0:
        try:
            return pymysql.connect(**DB_CONFIG)
        except pymysql.MySQLError:
            time.sleep(2)
            retries -= 1
    raise Exception("DB Connection Failed")

@app.route('/')
def index():
    # 1. Gestion du Cookie
    tracking_id = request.cookies.get('TrackingId')
    
    # Si pas de cookie, on en donne un valide
    if not tracking_id:
        resp = make_response(render_template('index.html', show_welcome=False))
        resp.set_cookie('TrackingId', 'auth_8f93j2k')
        return resp

    conn = get_db_connection()
    show_welcome = False

    try:
        with conn.cursor() as cursor:
            # 🚨 VULNERABLE BLIND QUERY
            # La requête vérifie juste si l'ID existe.
            # Payload : ' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>1)='a
            sql = f"SELECT id FROM tracking WHERE id = '{tracking_id}'"
            
            cursor.execute(sql)
            result = cursor.fetchone()
            
            if result:
                show_welcome = True
            
    except Exception:
        # BLIND : En cas d'erreur SQL, on n'affiche RIEN.
        # L'attaquant verra juste que le message "Welcome" a disparu.
        show_welcome = False
    finally:
        conn.close()

    return render_template('index.html', show_welcome=show_welcome)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Le flag est validé si on trouve le bon mot de passe
        if username == 'administrator' and password == '7b439c21':
            return render_template('login.html', success=True, flag="ESI-SBA{BL1ND_SQL1_BOOL3AN_M4ST3R}")
        else:
            error = "Invalid credentials."
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)