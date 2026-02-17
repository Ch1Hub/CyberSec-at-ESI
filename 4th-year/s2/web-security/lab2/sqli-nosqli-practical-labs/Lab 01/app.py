import time
import os
import pymysql
from flask import Flask, request, render_template

app = Flask(__name__)

# Récupération des variables d'environnement (définies dans docker-compose)
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'root')
DB_NAME = os.environ.get('DB_NAME', 'lab01')

def get_db_connection():
    # Boucle de retry pour attendre que le conteneur MySQL soit prêt
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
    raise Exception("❌ Impossible de se connecter à la BDD MySQL")

@app.route('/')
def index():
    category = request.args.get('category', 'All')
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if category == 'All':
                sql = "SELECT * FROM products WHERE released = 1"
                cursor.execute(sql)
            else:
                # 🚨 VULNÉRABILITÉ MAINTENUE (Concaténation)
                # Notez que pour MySQL, on utilise souvent le '#' pour commenter
                sql = f"SELECT * FROM products WHERE category = '{category}' AND released = 1"
                cursor.execute(sql)
            
            products = cursor.fetchall()
            return render_template('index.html', products=products, category=category)
            
    except pymysql.MySQLError as e:
        # Affiche l'erreur MySQL brute (très utile pour l'apprentissage)
        return render_template('index.html', error=str(e), products=[], category=category)
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)