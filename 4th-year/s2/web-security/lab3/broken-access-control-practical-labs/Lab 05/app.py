import time
import os
import pymysql
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'root')
DB_NAME = os.environ.get('DB_NAME', 'lab_bac_05')

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
    lab_solved = session.get('lab_solved', False)
    error = session.pop('error', None)
    return render_template('index.html', lab_solved=lab_solved, error=error)

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
                    return redirect(url_for('my_account', id=user['username']))
                else:
                    error = "Invalid credentials."
        finally:
            conn.close()

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# 🚨 VULNÉRABILITÉ IDOR (Horizontal Privilege Escalation)
@app.route('/my-account')
def my_account():
    # L'utilisateur doit être connecté...
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # ...mais on lit le profil demandé depuis l'URL (ex: ?id=amine)
    target_user = request.args.get('id')
    
    if not target_user:
        return redirect(url_for('my_account', id=session['username']))
        
    conn = get_db_connection()
    user_info = None
    try:
        with conn.cursor() as cursor:
            # On récupère les infos sans vérifier si session['username'] == target_user
            cursor.execute("SELECT id, username, api_key FROM users WHERE username = %s", (target_user,))
            user_info = cursor.fetchone()
    finally:
        conn.close()
        
    if not user_info:
        return "User not found", 404
        
    return render_template('profile.html', user=user_info)

@app.route('/submit-solution', methods=['POST'])
def submit_solution():
    api_key = request.form.get('api_key')
    if api_key == 'ESI-SBA{ID0R_AP1_K3Y_L34K}':
        session['lab_solved'] = True
    else:
        session['error'] = 'Invalid API Key. Try again!'
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)