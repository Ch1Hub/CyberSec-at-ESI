import time
import os
import pymysql
from flask import Flask, request, render_template

app = Flask(__name__)

# Config DB
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'root')
DB_NAME = os.environ.get('DB_NAME', 'lab03')

def get_db_connection():
    # On augmente la patience à 30 essais (soit env. 60 secondes)
    retries = 30
    while retries > 0:
        try:
            print(f"🔄 Connexion à {DB_HOST} (Tentative {31 - retries}/30)...")
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME,
                cursorclass=pymysql.cursors.DictCursor
            )
            return conn
        except pymysql.MySQLError as err:
            print(f"⏳ MySQL indisponible ({err}). Attente...")
            time.sleep(2)
            retries -= 1
    raise Exception("❌ Connection failed: Timeout après 60s")

@app.route('/')
def index():
    category = request.args.get('category', 'All')
    
    conn = get_db_connection()
    products = []
    error = None
    
    try:
        with conn.cursor() as cursor:
            # 🚨 VULNERABLE QUERY
            # Structure attendue : SELECT name, category FROM products WHERE category = '$cat'
            if category == 'All':
                sql = "SELECT name, category FROM products"
            else:
                # L'injection se fait ici.
                # L'étudiant va fermer la quote et ajouter UNION SELECT @@version, NULL #
                sql = f"SELECT name, category FROM products WHERE category = '{category}'"
            
            cursor.execute(sql)
            products = cursor.fetchall()
            
    except pymysql.MySQLError as e:
        error = str(e) # Affiche l'erreur pour aider au debug (UNION column mismatch)
    finally:
        conn.close()

    return render_template('index.html', products=products, category=category, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)