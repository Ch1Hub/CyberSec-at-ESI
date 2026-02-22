import time
import os
import pymysql
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'root')
DB_NAME = os.environ.get('DB_NAME', 'lab_bac_02')

# URL imprévisible pour le panel d'administration
SECRET_ADMIN_PATH = '/admin-panel-9k8m7n6p5q'

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
    # Vérifie si le lab est résolu (Djamel a-t-il été supprimé ?)
    conn = get_db_connection()
    lab_solved = False
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = 'djamel'")
            if not cursor.fetchone():
                lab_solved = True
    finally:
        conn.close()
        
    return render_template('index.html', lab_solved=lab_solved, admin_path=SECRET_ADMIN_PATH)

# 🚨 VULNÉRABILITÉ : La route est complexe, mais aucune vérification d'authentification n'est faite !
@app.route(SECRET_ADMIN_PATH)
def admin_panel():
    conn = get_db_connection()
    users = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
    finally:
        conn.close()
        
    return render_template('admin.html', users=users, admin_path=SECRET_ADMIN_PATH)

# La route de suppression utilise aussi le préfixe secret pour rester cohérente
@app.route(f'{SECRET_ADMIN_PATH}/delete/<username>')
def delete_user(username):
    if username == 'administrator':
        return "You cannot delete the administrator!", 403
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        conn.commit()
    finally:
        conn.close()
        
    return redirect(SECRET_ADMIN_PATH)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)