import time
import os
import pymysql
from flask import Flask, request, render_template

app = Flask(__name__)

# La chaîne aléatoire à injecter (définie dans docker-compose)
TARGET_STRING = os.environ.get('TARGET_STRING', 'x7k9p2')

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASS', 'root'),
    'database': os.environ.get('DB_NAME', 'lab07'),
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
    success = False

    try:
        with conn.cursor() as cursor:
            # La requête sélectionne 3 colonnes : id (INT), name (STR), stock (INT)
            if category == 'All':
                sql = "SELECT id, name, stock FROM products"
            else:
                # 🚨 VULNERABLE QUERY
                sql = f"SELECT id, name, stock FROM products WHERE category = '{category}'"
            
            cursor.execute(sql)
            products = cursor.fetchall()

            # --- SIMULATION DE TYPAGE STRICT (PEDAGOGIQUE) ---
            # Pour chaque ligne retournée, on vérifie les types.
            # MySQL laisse passer le texte dans un INT (ça vaut 0), mais Postgres/Oracle plantent.
            # On simule le plantage ici.
            for p in products:
                # Colonne 1 (id) doit être un nombre
                if not str(p['id']).isdigit():
                    raise Exception("Conversion failed when converting the varchar value to data type int.")
                
                # Colonne 3 (stock) doit être un nombre
                if not str(p['stock']).isdigit():
                    raise Exception("Conversion failed when converting the varchar value to data type int.")

                # Colonne 2 (name) : On vérifie si l'étudiant a réussi
                if p['name'] == TARGET_STRING:
                    success = True

    except Exception as e:
        # On affiche l'erreur comme le ferait une base de données stricte
        error = str(e)
    finally:
        conn.close()

    return render_template('index.html', products=products, category=category, error=error, success=success, target=TARGET_STRING)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)