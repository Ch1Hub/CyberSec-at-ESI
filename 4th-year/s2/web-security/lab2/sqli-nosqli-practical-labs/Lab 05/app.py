import time
import os
import pymysql
import re
from flask import Flask, request, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

# Config DB
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASS', 'root'),
    'database': os.environ.get('DB_NAME', 'lab05'),
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    # On augmente la patience à 30 tentatives de 2 secondes (60s total)
    retries = 30
    while retries > 0:
        try:
            print(f"🔄 Connexion à la BDD {DB_CONFIG['database']} ({31-retries}/30)...")
            return pymysql.connect(**DB_CONFIG)
        except pymysql.MySQLError as err:
            print(f"⏳ MySQL indisponible ({err}). Attente...")
            time.sleep(2)
            retries -= 1
    raise Exception("❌ DB Connection Failed: MySQL n'a pas démarré après 60 secondes.")

@app.route('/')
def index():
    category = request.args.get('category', 'All')
    error = None
    products = []
    
    # --- SIMULATION ORACLE (Pedagogique) ---
    if "UNION" in category.upper() and "FROM" not in category.upper():
        error = "ORA-00923: FROM keyword not found where expected"
    else:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                if category == 'All':
                    sql = "SELECT name, description FROM products"
                else:
                    # Injection ici.
                    sql = f"SELECT name, description FROM products WHERE category = '{category}'"
                
                cursor.execute(sql)
                products = cursor.fetchall()
        except pymysql.MySQLError as e:
            error_msg = str(e)
            if "different number of columns" in error_msg:
                error = "ORA-01789: query block has incorrect number of result columns"
            else:
                error = f"ORA-00933: SQL command not properly ended (Internal: {error_msg})"
        finally:
            conn.close()

    return render_template('index.html', products=products, category=category, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM USERS_Z9Y1 WHERE USERNAME_A1 = %s AND PASSWORD_B2 = %s"
                cursor.execute(sql, (username, password))
                user = cursor.fetchone()
                
                if user and user['USERNAME_A1'] == 'administrator':
                    return render_template('login.html', success=True, flag="ESI-SBA{ORACL3_S1MUL4T1ON_SUCC3SS}")
                else:
                    error = "Invalid credentials."
        finally:
            conn.close()

    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)