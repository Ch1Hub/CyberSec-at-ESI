import os
import re
import urllib.parse
import requests
import socket
from flask import Flask, request, render_template, make_response
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_key')

# Stockage en mémoire des interactions (pour ceux sans Burp Collaborator)
interaction_logs = []

def trigger_oob_interaction(target_url):
    """
    Simule l'action de la base de données qui contacte l'extérieur.
    Tente une résolution DNS et une requête HTTP.
    """
    domain = urllib.parse.urlparse(target_url).netloc
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    log_entry = {
        "time": timestamp,
        "target": target_url,
        "status": "Initiated"
    }
    
    try:
        # 1. Tentative DNS (Resolution)
        ip = socket.gethostbyname(domain)
        log_entry["dns_resolved"] = ip
        
        # 2. Tentative HTTP (Fire & Forget)
        # On met un timeout court pour ne pas bloquer l'app
        requests.get(target_url, timeout=2)
        log_entry["status"] = "Success (HTTP Request Sent)"
        
    except Exception as e:
        log_entry["status"] = f"Failed: {str(e)}"
    
    interaction_logs.insert(0, log_entry) # Ajouter au début de la liste

@app.route('/')
def index():
    tracking_id = request.cookies.get('TrackingId')
    
    if not tracking_id:
        resp = make_response(render_template('index.html'))
        resp.set_cookie('TrackingId', 'x')
        return resp

    # --- SIMULATION ORACLE VULNERABILITY ---
    # On décode l'URL (le cookie arrive souvent encodé depuis Burp)
    decoded_cookie = urllib.parse.unquote(tracking_id)
    
    # Regex pour détecter le payload Oracle du Lab 15
    # Cherche: EXTRACTVALUE(xmltype('...http://...'))
    # C'est une simplification pour le lab, une vraie DB parserait le XML.
    
    # Pattern: Cherche 'EXTRACTVALUE' suivi de 'http://' ou 'http%3a//'
    if "extractvalue" in decoded_cookie.lower() and "xmltype" in decoded_cookie.lower():
        # Extraction de l'URL cible via Regex
        # On cherche ce qu'il y a après SYSTEM " ou SYSTEM '
        match = re.search(r'SYSTEM\s+["\'](http[:s].*?)["\']', decoded_cookie, re.IGNORECASE)
        
        if match:
            target = match.group(1)
            # Correction des encodages fréquents dans les payloads SQLi
            target = target.replace('%3a', ':').replace('%3A', ':')
            target = target.replace('%2f', '/').replace('%2F', '/')
            
            print(f"[*] Oracle XXE Injection Detected! Target: {target}")
            trigger_oob_interaction(target)

    return render_template('index.html')

@app.route('/logs')
def logs():
    # Page bonus pour vérifier les hits si on n'a pas Burp Pro
    return render_template('logs.html', logs=interaction_logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)