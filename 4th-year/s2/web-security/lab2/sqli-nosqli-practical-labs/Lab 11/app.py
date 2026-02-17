import time
import os
import pymysql
from flask import Flask, request, render_template, make_response, abort

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASS', 'root'),
    'database': os.environ.get('DB_NAME', 'lab11'),
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
    tracking_id = request.cookies.get('TrackingId')
    
    # Cookie par défaut
    if not tracking_id:
        resp = make_response(render_template('index.html'))
        resp.set_cookie('TrackingId', 'xyz')
        return resp

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # --- CONFIGURATION ORACLE SIMULATION ---
            # 1. PIPES_AS_CONCAT : Pour que '||' fonctionne comme sur Oracle
            # 2. ERROR_FOR_DIVISION_BY_ZERO : Pour que 1/0 provoque une erreur fatale
            cursor.execute("SET sql_mode = 'PIPES_AS_CONCAT,ERROR_FOR_DIVISION_BY_ZERO,STRICT_TRANS_TABLES'")

            # --- NETTOYAGE PAYLOAD (Oracle -> MySQL) ---
            # MySQL n'a pas TO_CHAR. On l'enlève pour que seul le 1/0 à l'intérieur déclenche l'erreur.
            # L'étudiant tape : TO_CHAR(1/0)
            # MySQL reçoit : (1/0) -> Crash (ce qu'on veut)
            clean_id = tracking_id.replace('TO_CHAR', '').replace('to_char', '')

            # 🚨 VULNERABLE BLIND QUERY
            sql = f"SELECT id FROM tracking WHERE id = '{clean_id}'"
            
            # Exécution
            cursor.execute(sql)
            
            # Si on arrive ici, tout va bien -> HTTP 200
            return render_template('index.html')

    except Exception as e:
        print(f"SQL Error triggered: {e}") # Pour le debug prof dans la console
        # 🚨 CONDITION D'ERREUR
        # Si la requête plante (ex: 1/0), on renvoie une erreur 500
        return render_template('error.html'), 500
    finally:
        conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'administrator' and password == 'j98b23c71a32f5e8d90z':
            return render_template('login.html', success=True, flag="ESI-SBA{COND1T1ONAL_ERR0R_SQL1}")
        else:
            error = "Invalid credentials."
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)