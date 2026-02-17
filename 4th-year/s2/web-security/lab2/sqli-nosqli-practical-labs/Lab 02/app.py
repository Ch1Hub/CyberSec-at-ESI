import time
import os
import pymysql
from flask import Flask, request, render_template, session, redirect, url_for

app = Flask(__name__)

# Configuration via Variables d'Environnement
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_secret_key')
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'root')
DB_NAME = os.environ.get('DB_NAME', 'lab02')

def get_db_connection():
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
    raise Exception("❌ Impossible de se connecter à MySQL")

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # 🚨 VULNÉRABILITÉ MAJEURE 🚨
                # Injection SQL classique dans une clause WHERE
                # Payload étudiant : administrator' #
                query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
                
                cursor.execute(query)
                user = cursor.fetchone()
                
                if user:
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['role'] = user['role']
                    return redirect(url_for('dashboard'))
                else:
                    error = "Invalid username or password."
        except pymysql.MySQLError as e:
            error = f"SQL Error: {str(e)}"
        finally:
            conn.close()

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # On passe l'objet session directement au template
    return render_template('dashboard.html', user=session)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)