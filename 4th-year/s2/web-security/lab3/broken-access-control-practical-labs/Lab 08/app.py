import time
import os
import pymysql
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'root')
DB_NAME = os.environ.get('DB_NAME', 'lab_bac_08')

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
    # Vérification si le lab est résolu (Djamel a-t-il été supprimé ?)
    conn = get_db_connection()
    lab_solved = False
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = 'djamel'")
            if not cursor.fetchone():
                lab_solved = True
    finally:
        conn.close()
        
    return render_template('index.html', lab_solved=lab_solved)

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

# 🚨 VULNÉRABILITÉ : IDOR qui divulgue le mot de passe dans l'attribut HTML "value"
@app.route('/my-account')
def my_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    target_user = request.args.get('id')
    if not target_user:
        return redirect(url_for('my_account', id=session['username']))
        
    conn = get_db_connection()
    user_info = None
    try:
        with conn.cursor() as cursor:
            # Récupère les données (y compris le mot de passe) SANS vérifier les droits
            cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (target_user,))
            user_info = cursor.fetchone()
    finally:
        conn.close()
        
    if not user_info:
        return "User not found", 404
        
    return render_template('profile.html', user=user_info)

@app.route('/admin')
def admin_panel():
    if 'user_id' not in session or session.get('role') != 'admin':
        return render_template('unauthorized.html'), 401
        
    conn = get_db_connection()
    users = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, username, role FROM users")
            users = cursor.fetchall()
    finally:
        conn.close()
        
    return render_template('admin.html', users=users)

@app.route('/admin/delete/<username>')
def delete_user(username):
    if session.get('role') != 'admin':
        return "Unauthorized", 401
        
    if username == 'administrator':
        return "You cannot delete the administrator!", 403
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        conn.commit()
    finally:
        conn.close()
        
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)