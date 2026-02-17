import time
import os
import pymysql
from flask import Flask, request, render_template

app = Flask(__name__)

# Config DB
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASS', 'root'),
    'database': os.environ.get('DB_NAME', 'lab06'),
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    retries = 30
    while retries > 0:
        try:
            return pymysql.connect(**DB_CONFIG)
        except pymysql.MySQLError:
            print("⏳ Waiting for MySQL...")
            time.sleep(2)
            retries -= 1
    raise Exception("DB Connection Failed")

@app.route('/')
def index():
    category = request.args.get('category', 'All')
    conn = get_db_connection()
    products = []
    error = None
    success_msg = None

    try:
        with conn.cursor() as cursor:
            if category == 'All':
                # Requête de base pour tout afficher
                sql = "SELECT name, description, price FROM products"
                cursor.execute(sql)
            else:
                # 🚨 VULNERABLE QUERY
                # La requête sélectionne 3 colonnes : name, description, price
                # L'étudiant doit trouver ce chiffre magique "3".
                sql = f"SELECT name, description, price FROM products WHERE category = '{category}'"
                cursor.execute(sql)
            
            products = cursor.fetchall()

            # --- LOGIQUE DE DÉTECTION DE SUCCÈS (Pour le fun) ---
            # Si on trouve une ligne qui contient des NULLs partout (ce qui arrive quand on fait UNION SELECT NULL, NULL, NULL)
            # alors l'étudiant a réussi l'exercice.
            for p in products:
                # Vérifie si toutes les valeurs de la ligne sont None (NULL en SQL)
                if p['name'] is None and p['description'] is None and p['price'] is None:
                    success_msg = "🎉 CONGRATULATIONS! You determined the correct number of columns (3)."

    except pymysql.MySQLError as e:
        # Affiche l'erreur MySQL brute (The used SELECT statements have a different number of columns)
        error = str(e)
    finally:
        conn.close()

    return render_template('index.html', products=products, category=category, error=error, success_msg=success_msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)