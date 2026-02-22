import time
import os
import pymysql
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'root')
DB_NAME = os.environ.get('DB_NAME', 'lab_bac_11')

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
                cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
                user = cursor.fetchone()
                
                if user:
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['role'] = user['role']
                    return redirect(url_for('index'))
                else:
                    error = "Invalid credentials."
        finally:
            conn.close()

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin')
def admin_panel():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if session.get('role') != 'admin':
        return "Unauthorized: Admins only", 401
        
    conn = get_db_connection()
    users = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, username, role FROM users")
            users = cursor.fetchall()
    finally:
        conn.close()
        
    return render_template('admin.html', users=users)

# 🚨 VULNÉRABILITÉ : Contrôle d'accès basé uniquement sur la méthode POST
# Note : POSTX est ajouté explicitement pour permettre à l'étudiant de reproduire l'étape du lab.
@app.route('/admin/promote', methods=['GET', 'POST', 'POSTX'])
def promote():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # Le développeur n'a protégé que la méthode POST (celle utilisée par le formulaire)
    if request.method == 'POST':
        if session.get('role') != 'admin':
            return "Unauthorized", 401
            
    # Si la méthode est GET ou POSTX, le contrôle ci-dessus est silencieusement ignoré !

    # request.values cherche dans les paramètres d'URL (GET) et dans le Body (POST).
    # Cependant, Flask ne parse le Body que pour les méthodes POST/PUT/PATCH.
    # - Si la méthode est POSTX : le corps n'est pas parsé, request.values est vide -> "missing parameter".
    # - Si la méthode est GET : l'URL est parsée, request.values trouve le paramètre -> Succès !
    username = request.values.get('username')
    
    if not username:
        return "missing parameter", 400
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE users SET role = 'admin' WHERE username = %s", (username,))
        conn.commit()
        
        # Mise à jour de la session si l'utilisateur s'est auto-promu
        if username == session.get('username'):
            session['role'] = 'admin'
            session['lab_solved'] = True
            
    finally:
        conn.close()
        
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)