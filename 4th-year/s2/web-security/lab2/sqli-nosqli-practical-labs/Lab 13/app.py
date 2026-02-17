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
    'dbname': os.environ.get('DB_NAME', 'lab13')
}

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception:
        return None

@app.route('/')
def index():
    tracking_id = request.cookies.get('TrackingId')
    
    # Cookie par défaut
    if not tracking_id:
        resp = make_response(render_template('index.html'))
        resp.set_cookie('TrackingId', 'x')
        return resp

    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                # 🚨 VULNERABLE QUERY
                # Injection directe.
                # Même si la requête plante (ex: concaténation string + void),
                # PostgreSQL évalue souvent la fonction pg_sleep() AVANT de lever l'erreur.
                sql = f"SELECT * FROM tracking WHERE id = '{tracking_id}'"
                
                cursor.execute(sql)
                # On ne fait rien du résultat
        except Exception as e:
            # BLIND TOTAL : On ignore silencieusement toutes les erreurs.
            # L'utilisateur ne verra jamais si la requête a planté ou réussi.
            pass
        finally:
            conn.close()

    # On renvoie toujours la même page, quoi qu'il arrive.
    return render_template('index.html')

if __name__ == '__main__':
    # Threaded=True est important pour ne pas bloquer tout le serveur pendant le sleep
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)