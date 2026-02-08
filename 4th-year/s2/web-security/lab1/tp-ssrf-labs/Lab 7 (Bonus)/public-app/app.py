# public-app/app.py
from flask import Flask, request, jsonify
import requests
import socket
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        target_url = request.form.get('url')
        
        if not target_url:
            return "Missing URL", 400

        # FILTRE DE SÉCURITÉ (Basic)
        # L'étudiant doit comprendre qu'il doit cibler le réseau interne, pas localhost
        domain = urlparse(target_url).hostname
        if domain in ['localhost', '127.0.0.1', '::1', '0.0.0.0']:
             return "Blocked for security reasons.", 403

        try:
            # VULNÉRABILITÉ BLIND SSRF
            # On fait la requête, mais on n'affiche PAS la réponse (r.text)
            # Timeout court pour permettre l'analyse Time-Based
            r = requests.get(target_url, timeout=3)
            
            # Le serveur répond toujours "Success" peu importe le code retour (200, 404, 500)
            return jsonify({"status": "success", "message": "Webhook triggered!"})
        
        except requests.exceptions.Timeout:
            # Fuite d'information subtile : Le timeout est distinct de l'erreur de connexion
            return jsonify({"status": "error", "message": "Target timed out"}), 504
        except:
            return jsonify({"status": "error", "message": "Connection failed"}), 500

    return """
    <h1>Internal Webhook Tester</h1>
    <form method="POST">
        <label>Enter Webhook URL to test:</label><br>
        <input type="text" name="url" size="50">
        <input type="submit" value="Test Connectivity">
    </form>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)