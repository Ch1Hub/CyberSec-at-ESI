import time
import os
import pymysql
from flask import Flask, request, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

# Config DB
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'root')
DB_NAME = os.environ.get('DB_NAME', 'lab04')

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
            # 🚨 VULNERABLE QUERY (UNION BASED)
            # L'étudiant doit injecter ici pour lister les tables
            if category == 'All':
                sql = "SELECT name, description FROM products"
            else:
                # Injection : ' UNION SELECT table_name, NULL FROM information_schema.tables #
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
        # Ici c'est un login "Propre" (sécurisé)
        # Le but n'est pas de bypasser le login par SQLi, mais d'utiliser
        # le mot de passe trouvé via l'autre faille.
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # On doit utiliser les vrais noms de colonnes bizarres pour vérifier
                # Mais l'étudiant ne le sait pas, il doit juste entrer le bon pass.
                sql = "SELECT * FROM users_x9d2k WHERE username_u8s1 = %s AND password_p4w9 = %s"
                cursor.execute(sql, (username, password)) # Requête paramétrée SÉCURISÉE
                user = cursor.fetchone()
                
                if user and user['username_u8s1'] == 'administrator':
                    return render_template('login.html', success=True, flag="ESI-SBA{M4PP1NG_M4ST3R_DB_HACK3R}")
                elif user:
                    error = "Logged in as user, but you are not admin!"
                else:
                    error = "Invalid credentials."
        finally:
            conn.close()

    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)