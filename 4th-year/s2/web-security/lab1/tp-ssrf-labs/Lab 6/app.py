from flask import Flask, request, render_template
import requests
import threading
import time
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURATION ---
# Stockage des logs pour simuler l'interface "Collaborator" 
# si l'étudiant n'a pas accès à internet depuis le container.
OUTGOING_REQUESTS_LOG = []

# --- MOCK DATABASE ---
PRODUCTS = [
    {"id": 1, "name": "HackRF One", "price": "300 $", "image": "https://shop.hak5.org/cdn/shop/products/hackrf-one_530x@2x.jpg", "desc": "SDR Platform"},
    {"id": 2, "name": "Ubertooth One", "price": "120 $", "image": "https://shop.hak5.org/cdn/shop/products/ubertooth-one_530x@2x.jpg", "desc": "Bluetooth Sniffing"},
    {"id": 3, "name": "Yard Stick One", "price": "100 $", "image": "https://shop.hak5.org/cdn/shop/products/yard-stick-one_530x@2x.jpg", "desc": "Sub-1 GHz Wireless"},
]

def analytics_worker(referer_url):
    """
    Simule le moteur d'analytics qui va visiter le lien Referer.
    Ceci se passe en arrière-plan (Blind).
    """
    log_entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "target": referer_url,
        "status": "PENDING"
    }
    OUTGOING_REQUESTS_LOG.insert(0, log_entry) # Ajout au début de liste
    
    try:
        # Le serveur tente de se connecter à l'URL fournie (SSRF)
        # Timeout court pour ne pas bloquer le thread trop longtemps
        r = requests.get(referer_url, timeout=3, headers={"User-Agent": "AnalyticsBot/1.0"})
        log_entry["status"] = f"SUCCESS ({r.status_code})"
    except Exception as e:
        log_entry["status"] = f"FAILED ({str(e)})"

@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404

    # --- VULNÉRABILITÉ BLIND SSRF ---
    # L'application lit le header 'Referer' pour ses statistiques.
    referer = request.headers.get('Referer')
    
    if referer:
        # On lance la tâche en fond (Fire and Forget)
        # L'utilisateur ne verra jamais le résultat de cette requête sur sa page.
        thread = threading.Thread(target=analytics_worker, args=(referer,))
        thread.start()

    return render_template('product.html', product=product)

# --- ROUTE DE MONITORING (Pour aider l'étudiant) ---
# Dans la vraie vie, c'est le serveur de l'attaquant (Burp Collaborator / Webhook.site).
# Ici, on fournit une page interne pour voir ce que le serveur a fait.
@app.route('/admin/analytics-monitor')
def monitor():
    return render_template('monitor.html', logs=OUTGOING_REQUESTS_LOG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)