import time
import os
import pymysql
from flask import Flask, request, render_template, redirect, url_for, make_response

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'root')
DB_NAME = os.environ.get('DB_NAME', 'lab_bac_03')

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
    conn = get_db_connection()
    lab_solved = False
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = 'djamel'")
            if not cursor.fetchone():
                lab_solved = True
    finally:
        conn.close()
        
    username = request.cookies.get('Username')
    return render_template('index.html', lab_solved=lab_solved, current_user=username)

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
                    # 🚨 VULNÉRABILITÉ : On stocke le rôle en clair dans un cookie
                    resp = make_response(redirect(url_for('index')))
                    resp.set_cookie('Username', user['username'])
                    
                    if user['role'] == 'admin':
                        resp.set_cookie('AdminRole', 'true')
                    else:
                        resp.set_cookie('AdminRole', 'false')
                        
                    return resp
                else:
                    error = "Invalid credentials."
        finally:
            conn.close()

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('Username')
    resp.delete_cookie('AdminRole')
    return resp

@app.route('/admin')
def admin_panel():
    # 🚨 VULNÉRABILITÉ : L'accès dépend uniquement de la valeur d'un cookie modifiable
    is_admin = request.cookies.get('AdminRole')
    
    if is_admin != 'true':
        return render_template('unauthorized.html'), 401
        
    conn = get_db_connection()
    users = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
    finally:
        conn.close()
        
    return render_template('admin.html', users=users)

@app.route('/admin/delete/<username>')
def delete_user(username):
    # On revérifie la vulnérabilité sur l'action de suppression
    if request.cookies.get('AdminRole') != 'true':
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