import time
import os
import pymysql
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

# Config DB
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASS', 'root'),
    'database': os.environ.get('DB_NAME', 'lab08'),
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
            # La requête sélectionne 2 colonnes : name, description
            if category == 'All':
                sql = "SELECT name, description FROM products"
            else:
                # 🚨 VULNERABLE QUERY
                # L'injection va se faire ici pour coller les users à la suite des produits
                sql = f"SELECT name, description FROM products WHERE category = '{category}'"
            
            cursor.execute(sql)
            products = cursor.fetchall()
            
    except pymysql.MySQLError as e:
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
        
        # Vérification simple pour valider le flag
        if username == 'administrator' and password == 'Sup3r_S3cr3t_P@ssw0rd_Retrieved!':
            return render_template('login.html', success=True, flag="ESI-SBA{UN10N_DUMP_SUCC3SS}")
        else:
            error = "Invalid credentials. Did you find the admin password?"

    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)