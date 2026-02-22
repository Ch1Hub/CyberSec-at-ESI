import time
import os
import pymysql
from flask import Flask, request, render_template, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'root')
DB_NAME = os.environ.get('DB_NAME', 'lab_bac_04')

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
                    session['roleid'] = user['roleid']
                    return redirect(url_for('my_account'))
                else:
                    error = "Invalid credentials."
        finally:
            conn.close()

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/my-account')
def my_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    user_info = {}
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
            user_info = cursor.fetchone()
    finally:
        conn.close()
        
    return render_template('profile.html', user=user_info)

# 🚨 VULNÉRABILITÉ DE MASS ASSIGNMENT (JSON)
@app.route('/update-profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updates = []
    values = []
    
    # Le backend accepte aveuglément toutes les clés fournies dans le JSON
    # et met à jour la base de données. Il n'y a pas de liste blanche stricte
    # empêchant la modification de 'roleid'.
    for key, value in data.items():
        if key in ['email', 'roleid']: # Autorise techniquement roleid à être modifié
            updates.append(f"{key} = %s")
            values.append(value)
            
    if updates:
        values.append(session['user_id'])
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, tuple(values))
            conn.commit()
            
            # Mise à jour de la session si roleid a été injecté
            if 'roleid' in data:
                session['roleid'] = int(data['roleid'])
                
        finally:
            conn.close()

    return jsonify({"message": "Profile updated successfully!", "roleid": session.get('roleid')})

@app.route('/admin')
def admin_panel():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # Vérification stricte du roleid = 2 pour l'accès
    if session.get('roleid') != 2:
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
    if session.get('roleid') != 2:
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