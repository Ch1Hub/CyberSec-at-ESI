# internal-admin/app.py
from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Chargement du flag dynamique
try:
    with open('/flag.txt', 'r') as f:
        FLAG = f.read().strip()
except:
    FLAG = "ESI-SBA{TEST_FLAG}"

@app.route('/')
def home():
    return "Internal Admin Panel - v1.0"

# Endpoint caché que l'étudiant doit deviner ou fuzz
# Dans un vrai TP, on pourrait donner un indice que l'API est "/admin/forward_flag"
@app.route('/admin/forward_flag', methods=['GET'])
def forward_flag():
    # L'attaquant fournit son URL externe (dest)
    destination = request.args.get('dest')
    
    if destination:
        try:
            # Le service interne envoie le flag à l'attaquant (OOB)
            requests.post(destination, data={'secret_flag': FLAG}, timeout=2)
            return "Flag forwarded!"
        except:
            return "Failed to forward"
    return "Missing 'dest' parameter"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)