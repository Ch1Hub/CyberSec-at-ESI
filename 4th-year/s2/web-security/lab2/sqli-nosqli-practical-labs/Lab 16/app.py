import os
import re
import urllib.parse
from flask import Flask, request, render_template, make_response, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

# Le secret à voler
ADMIN_PASSWORD = "hz49d2e8b1c7f0a3g6k5" 

# Logs en mémoire pour remplacer Burp Collaborator
oob_logs = []

@app.route('/')
def index():
    tracking_id = request.cookies.get('TrackingId')
    
    if not tracking_id:
        resp = make_response(render_template('index.html'))
        resp.set_cookie('TrackingId', 'x')
        return resp

    # --- SIMULATION ORACLE EXFILTRATION ---
    decoded_cookie = urllib.parse.unquote(tracking_id)
    
    # On cherche le pattern Oracle XXE : EXTRACTVALUE + xmltype + http
    if "extractvalue" in decoded_cookie.lower() and "xmltype" in decoded_cookie.lower():
        
        # 1. Extraction de la structure de l'URL injectée
        # Le payload ressemble à : ... SYSTEM "http://" || (SELECT...) || ".collab.net" ...
        # On essaie de capturer ce qui est entre les guillemets du SYSTEM
        
        # Simplification pour la simulation : On cherche la structure concaténée
        # On cherche un bloc qui commence par http et finit par un domaine, avec des || au milieu
        
        target_domain = "unknown-interaction"
        exfiltrated_data = None

        # Simulation de l'exécution SQL dynamique
        # Si l'utilisateur a injecté: (SELECT password FROM users WHERE username='administrator')
        # ou une variante proche, on remplace ce bloc par le vrai mot de passe.
        
        # Regex souple pour détecter la requête SQL du lab
        sql_pattern = r"\(SELECT\s+password\s+FROM\s+users\s+WHERE\s+username\s*=\s*'administrator'\)"
        
        if re.search(sql_pattern, decoded_cookie, re.IGNORECASE):
            # C'est la bonne requête !
            # Maintenant on regarde le domaine de fin.
            # On cherche ce qui est après le dernier ||
            # Format attendu: ... || '.BURP-COLLABORATOR-SUBDOMAIN'
            
            domain_match = re.search(r"\|\|\s*'[\.]?([a-zA-Z0-9\.-]+)'", decoded_cookie)
            if domain_match:
                collaborator_domain = domain_match.group(1)
                
                # La base de données concatène : "http://" + PASSWORD + "." + DOMAINE
                generated_url = f"http://{ADMIN_PASSWORD}.{collaborator_domain}"
                
                # On loggue l'interaction
                log_entry = {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "query_type": "DNS/HTTP",
                    "raw_url": generated_url,
                    "exfiltrated_data": ADMIN_PASSWORD, # Pour aider l'étudiant à comprendre
                    "target_domain": collaborator_domain
                }
                oob_logs.insert(0, log_entry)

    return render_template('index.html')

@app.route('/logs')
def logs():
    return render_template('logs.html', logs=oob_logs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'administrator' and password == ADMIN_PASSWORD:
            return render_template('login.html', success=True, flag="ESI-SBA{OOB_EXF1L_M4ST3R}")
        else:
            error = "Invalid credentials."
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)