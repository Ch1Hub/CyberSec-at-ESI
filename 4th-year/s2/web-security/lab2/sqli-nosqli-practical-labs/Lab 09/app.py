import time
import os
import pymysql
from flask import Flask, request, render_template

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASS', 'root'),
    'database': os.environ.get('DB_NAME', 'lab09'),
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
    category = request.args.get('category', 'All')
    conn = get_db_connection()
    products = []
    error = None

    try:
        with conn.cursor() as cursor:
            # La requête sélectionne 2 colonnes : id (INT), name (STRING)
            if category == 'All':
                sql = "SELECT id, name FROM products"
            else:
                # 🚨 VULNERABLE QUERY
                sql = f"SELECT id, name FROM products WHERE category = '{category}'"
            
            cursor.execute(sql)
            products = cursor.fetchall()

            # --- STRICT TYPE CHECKING SIMULATION ---
            # On force l'étudiant à respecter les types de colonnes
            for p in products:
                # La colonne 1 (id) DOIT être un nombre.
                # Si l'étudiant injecte "username" ici, ça plantera.
                if not str(p['id']).isdigit() and p['id'] is not None:
                     raise Exception("Data Conversion Error: Column 1 expects Integer, got String.")
                
    except Exception as e:
        error = str(e)
    finally:
        conn.close()

    return render_template('index.html', products=products, category=category, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'administrator' and password == 'Complex_P@ss_With_C0ncat!':
            return render_template('login.html', success=True, flag="ESI-SBA{C0NCAT3NAT10N_K1NG}")
        else:
            error = "Invalid credentials."
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)