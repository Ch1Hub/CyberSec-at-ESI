import sqlite3
import random
import string
from flask import Flask, request, render_template

app = Flask(__name__)

# Configuration de la base de données en mémoire
# check_same_thread=False est nécessaire car Flask est multi-thread
conn = sqlite3.connect(':memory:', check_same_thread=False)
c = conn.cursor()

def init_db():
    # 1. Génération de 50 tables bidons (Le bruit)
    # On garde les noms pour ne pas perdre la trace, mais le hacker ne les connait pas
    for i in range(50):
        # random name like table_a1b2c3d4
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        table_name = f"table_{suffix}"
        c.execute(f"CREATE TABLE {table_name} (dummy_col TEXT)")
        c.execute(f"INSERT INTO {table_name} VALUES ('nothing_here')")

    # 2. La table du flag (L'aiguille dans la botte de foin)
    c.execute("DROP TABLE IF EXISTS super_hidden_table_x99")
    c.execute("CREATE TABLE super_hidden_table_x99 (secret_flag_col TEXT)")
    c.execute("INSERT INTO super_hidden_table_x99 VALUES ('FLAG{SQLMAP_AUTO_DUMP_KING}')")
    
    conn.commit()
    print("[+] Database initialized with 50 dummy tables and 1 hidden flag table.")

# On initialise la DB au démarrage
init_db()

@app.route('/')
def index():
    cat = request.args.get('cat')

    # CAS 1 : Pas de paramètre ? On affiche l'interface graphique.
    if not cat:
        return render_template('index.html')

    # CAS 2 : Paramètre présent ? On tente l'injection SQL.
    # C'est ici que SQLMap va travailler.
    try:
        # Injection SQL Booléenne (Blind)
        # Si cat = "1", la requête est SELECT 1 WHERE 1=1 (VRAI)
        # Si cat = "1 AND 1=0", la requête est SELECT 1 WHERE 1=1 AND 1=0 (FAUX)
        query = f"SELECT 1 WHERE 1={cat}"
        
        # On exécute (attention, c'est très vulnérable !)
        cursor = c.execute(query)
        result = cursor.fetchone()
        
        if result:
            return "Product exists." # Signal TRUE pour SQLMap
        else:
            return "Product missing." # Signal FALSE pour SQLMap (ou pas de résultat)
            
    except Exception as e:
        # En cas d'erreur SQL (syntaxe invalide injectée), on renvoie Missing
        return "Product missing." 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)