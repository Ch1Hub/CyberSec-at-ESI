import time
import os
import pymysql
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'root')
DB_NAME = os.environ.get('DB_NAME', 'lab_bac_06')

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
    
    # Récupérer les articles de blog
    conn = get_db_connection()
    posts = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.title, p.content, p.author_guid, u.username 
                FROM posts p 
                JOIN users u ON p.author_guid = u.guid
            """)
            posts = cursor.fetchall()
    finally:
        conn.close()
        
    return render_template('index.html', lab_solved=lab_solved, error=error, posts=posts)

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
                    session['guid'] = user['guid']
                    session['username'] = user['username']
                    return redirect(url_for('my_account', id=user['guid']))
                else:
                    error = "Invalid credentials."
        finally:
            conn.close()

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/author')
def author_profile():
    # Profil PUBLIC de l'auteur
    author_guid = request.args.get('id')
    if not author_guid:
        return redirect(url_for('index'))
        
    conn = get_db_connection()
    author = None
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT username FROM users WHERE guid = %s", (author_guid,))
            author = cursor.fetchone()
    finally:
        conn.close()
        
    if not author:
        return "Author not found", 404
        
    return render_template('author.html', author=author)

# 🚨 VULNÉRABILITÉ IDOR (Horizontal Privilege Escalation avec GUID)
@app.route('/my-account')
def my_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # Le paramètre vulnérable
    target_guid = request.args.get('id')
    
    if not target_guid:
        return redirect(url_for('my_account', id=session['guid']))
        
    conn = get_db_connection()
    user_info = None
    try:
        with conn.cursor() as cursor:
            # On récupère les infos sensibles SANS vérifier si session['guid'] == target_guid
            cursor.execute("SELECT id, guid, username, api_key FROM users WHERE guid = %s", (target_guid,))
            user_info = cursor.fetchone()
    finally:
        conn.close()
        
    if not user_info:
        return "User not found", 404
        
    return render_template('profile.html', user=user_info)

@app.route('/submit-solution', methods=['POST'])
def submit_solution():
    api_key = request.form.get('api_key')
    if api_key == 'ESI-SBA{UNPR3D1CT4BL3_ID0R_M4ST3R}':
        session['lab_solved'] = True
    else:
        session['error'] = 'Invalid API Key. Try again!'
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)