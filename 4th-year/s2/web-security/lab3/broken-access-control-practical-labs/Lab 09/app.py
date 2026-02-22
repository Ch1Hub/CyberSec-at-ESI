import time
import os
import pymysql
from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'root')
DB_NAME = os.environ.get('DB_NAME', 'lab_bac_09')

# --- CONFIGURATION CHAT LOGS ---
CHAT_DIR = 'chat_logs'
os.makedirs(CHAT_DIR, exist_ok=True)

# Création du fichier log compromettant (IDOR cible)
with open(os.path.join(CHAT_DIR, '1.txt'), 'w', encoding='utf-8') as f:
    f.write("--- TRANSCRIPT STARTED ---\n")
    f.write("Support: Hello, how can I help you today?\n")
    f.write("Djamel: Hi, I forgot my password and I urgently need to access my account.\n")
    f.write("Support: No problem, let me check your identity...\n")
    f.write("Support: OK, I have reset it for you.\n")
    f.write("Support: Your temporary password is 'P@ssw0rd_Dj4m3l_2026'. Please log in and keep it safe.\n")
    f.write("Djamel: Thanks a lot!\n")
    f.write("--- TRANSCRIPT ENDED ---\n")
# -------------------------------

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
                    
                    # Si on se connecte en tant que Djamel, le lab est résolu !
                    if user['username'] == 'djamel':
                        session['lab_solved'] = True
                        
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

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    transcript_file = None
    if request.method == 'POST':
        user_message = request.form.get('message')
        # On simule un compteur pour l'historique du visiteur actuel
        # Le système lui attribue le fichier "2.txt" car "1.txt" existe déjà
        transcript_file = '2.txt'
        
        filepath = os.path.join(CHAT_DIR, transcript_file)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("--- TRANSCRIPT STARTED ---\n")
            f.write(f"You: {user_message}\n")
            f.write("Support: Thank you for reaching out. An agent will contact you shortly via email.\n")
            f.write("--- TRANSCRIPT ENDED ---\n")
            
    return render_template('chat.html', transcript=transcript_file)

# 🚨 VULNÉRABILITÉ : Insecure Direct Object Reference (IDOR) sur fichier statique
@app.route('/download-transcript/<filename>')
def download_transcript(filename):
    # L'application renvoie le fichier demandé sans vérifier l'autorisation de l'utilisateur.
    # Un attaquant peut simplement demander '1.txt'.
    return send_from_directory(CHAT_DIR, filename, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)