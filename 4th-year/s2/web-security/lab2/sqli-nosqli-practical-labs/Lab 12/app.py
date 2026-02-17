import time
import os
import psycopg2 # Driver PostgreSQL
import psycopg2.extras
from flask import Flask, request, render_template, make_response

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASS', 'root'),
    'dbname': os.environ.get('DB_NAME', 'lab12')
}

# Simulation d'une limite de WAF ou de buffer
COOKIE_LENGTH_LIMIT = 100 

def get_db_connection():
    retries = 30
    while retries > 0:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            return conn
        except psycopg2.OperationalError:
            time.sleep(2)
            retries -= 1
    raise Exception("DB Connection Failed")

@app.route('/')
def index():
    tracking_id = request.cookies.get('TrackingId')
    
    if not tracking_id:
        resp = make_response(render_template('index.html'))
        resp.set_cookie('TrackingId', 'ogAZZfxtOKUELbuJ')
        return resp

    conn = get_db_connection()
    # Par défaut, pas d'erreur
    db_error = None
    
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            
            # 1. TRUNCATION SIMULATION
            # L'énoncé dit que la requête est coupée si elle est trop longue.
            # On simule ça ici pour forcer l'étudiant à optimiser son payload.
            if len(tracking_id) > COOKIE_LENGTH_LIMIT:
                tracking_id = tracking_id[:COOKIE_LENGTH_LIMIT]
                # On ajoute un marqueur visuel pour dire que ça a coupé (facultatif mais pédagogique)
                # db_error = "Warning: Input truncated by server limit."

            # 2. VULNERABLE QUERY
            sql = f"SELECT * FROM tracking WHERE id = '{tracking_id}'"
            
            cursor.execute(sql)
            # On se fiche du résultat, on veut juste voir si ça plante
            
    except Exception as e:
        # 🚨 VULNERABILITÉ ICI : On affiche l'erreur brute à l'utilisateur
        # PostgreSQL renvoie des erreurs très bavardes.
        db_error = str(e)
    finally:
        conn.close()

    return render_template('index.html', error=db_error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'administrator' and password == 'postgres_error_leaks_secrets':
            return render_template('login.html', success=True, flag="ESI-SBA{P0STGR3S_C4ST_ERR0R_L34K}")
        else:
            error = "Invalid credentials."
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)