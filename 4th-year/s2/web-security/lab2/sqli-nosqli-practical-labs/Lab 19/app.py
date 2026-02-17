import sqlite3
import time
import os  # <--- C'était l'import manquant !
from flask import Flask, request

app = Flask(__name__)

# Nom du fichier de base de données
DB_FILE = "lab19.db"

def init_db():
    # Suppression de l'ancienne base pour repartir à zéro à chaque redémarrage
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
        except Exception as e:
            print(f"Warning: Could not delete old DB: {e}")

    # Création de la nouvelle base
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()
    
    # Table des logs (Cible de l'injection)
    c.execute("CREATE TABLE admin_logs (id INTEGER PRIMARY KEY, user_agent TEXT)")
    
    # Table cachée contenant le flag
    c.execute("CREATE TABLE sensitive_data (login TEXT, password TEXT)")
    c.execute("INSERT INTO sensitive_data VALUES ('admin', 'FLAG{SQLMAP_STACKED_QUERIES_MASTER}')")
    
    conn.commit()
    conn.close()

# Initialisation au démarrage
init_db()

@app.route('/')
def index():
    ua = request.headers.get('User-Agent', '')
    
    # Connexion à la DB pour chaque requête (plus stable pour sqlmap)
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()
    
    try:
        # VULNÉRABILITÉ : Injection SQL via User-Agent
        # Utilisation de executescript() qui permet les "Stacked Queries" (requêtes multiples séparées par ;)
        query = f"INSERT INTO admin_logs (user_agent) VALUES ('{ua}')"
        
        # Le script exécute la requête sans vérification
        c.executescript(query)
        conn.commit()
        return "Logged."
        
    except Exception as e:
        # En cas d'erreur SQL, on retourne une erreur générique
        return f"Error Logging."
        
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)