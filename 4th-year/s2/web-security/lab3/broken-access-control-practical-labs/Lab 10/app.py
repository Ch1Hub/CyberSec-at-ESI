import time
import os
import pymysql
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'root')
DB_NAME = os.environ.get('DB_NAME', 'lab_bac_10')

def get_db_connection():
    retries = 30
    while retries > 0:
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME,
                cursorclass=pymysql.cursors.DictCursor
            )
            return conn
        except pymysql.MySQLError:
            print("⏳ Waiting for MySQL database...")
            time.sleep(2)
            retries -= 1
    raise Exception("❌ Impossible de se connecter à MySQL")

# 🚨 SIMULATION DE L'ARCHITECTURE VULNÉRABLE (Front-end vs Back-end)
class ProxySimulatorMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')

        # 1. Front-end WAF Simulator : Bloque tout ce qui commence par /admin
        if path.startswith('/admin'):
            start_response('403 Forbidden', [('Content-Type', 'text/plain')])
            return [b"403 Forbidden - Access Denied by Front-End Proxy"]

        # 2. Back-end Framework Simulator : Respecte le header X-Original-URL
        # Dans le standard WSGI, les headers HTTP sont préfixés par HTTP_
        x_original_url = environ.get('HTTP_X_ORIGINAL_URL')
        if x_original_url:
            # Réécrit silencieusement le chemin pour le routeur Flask
            environ['PATH_INFO'] = x_original_url

        return self.wsgi_app(environ, start_response)

# Application du middleware au-dessus de l'application Flask
app.wsgi_app = ProxySimulatorMiddleware(app.wsgi_app)

@app.route('/')
def index():
    # Vérifie si le lab est résolu
    conn = get_db_connection()
    lab_solved = False
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = 'djamel'")
            if not cursor.fetchone():
                lab_solved = True
    finally:
        conn.close()
        
    return render_template('index.html', lab_solved=lab_solved)

@app.route('/admin')
def admin_panel():
    conn = get_db_connection()
    users = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, username, role FROM users")
            users = cursor.fetchall()
    finally:
        conn.close()
        
    return render_template('admin.html', users=users)

@app.route('/admin/delete')
def delete_user():
    # Suppression via un paramètre GET dans la vraie query string
    username = request.args.get('username')
    if not username:
        return "Missing username parameter", 400
        
    if username == 'administrator':
        return "Cannot delete administrator!", 403
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        conn.commit()
    finally:
        conn.close()
        
    # On renvoie du texte plutôt qu'une redirection, car si l'étudiant est 
    # dans Burp, la redirection vers /admin serait bloquée par le WAF.
    return f"User '{username}' deleted successfully! Return to / to check your lab status.", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)