import time
import os
import psycopg2
from flask import Flask, request, render_template, make_response

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASS', 'root'),
    'dbname': os.environ.get('DB_NAME', 'lab14')
}

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception:
        return None

@app.route('/')
def index():
    tracking_id = request.cookies.get('TrackingId')
    
    if not tracking_id:
        resp = make_response(render_template('index.html'))
        resp.set_cookie('TrackingId', 'x')
        return resp

    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                # 🚨 VULNERABLE QUERY (Stacked Queries allowed in Postgres via injection)
                # Payload type: x'; SELECT CASE WHEN (cond) THEN pg_sleep(5) ELSE pg_sleep(0) END--
                sql = f"SELECT * FROM tracking WHERE id = '{tracking_id}'"
                
                cursor.execute(sql)
                # On ignore le résultat.
        except Exception:
            # On ignore les erreurs.
            pass
        finally:
            conn.close()

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Validation du Flag
        if username == 'administrator' and password == 't1m3_i5_k3y!':
            return render_template('login.html', success=True, flag="ESI-SBA{T1ME_B4SED_EXF1LTR4T1ON_K1NG}")
        else:
            error = "Invalid credentials. Keep enumerating!"
    return render_template('login.html', error=error)

if __name__ == '__main__':
    # Threaded=True pour gérer plusieurs requêtes (attaque Intruder) simultanément
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)