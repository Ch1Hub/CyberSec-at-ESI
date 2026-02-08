from flask import Flask, request, render_template, jsonify
from urllib.parse import urlparse
import requests

app = Flask(__name__)

# --- CONFIGURATION DU CHALLENGE ---
# C'est l'IP secrète que les étudiants doivent trouver via Burp Intruder
INTERNAL_HIDDEN_IP = "192.168.0.211"
INTERNAL_PORT = 8080

# --- MOCK DATABASE ---
PRODUCTS = [
    {"id": 1, "name": "Flippper Zero", "price": "169 $", "image": "https://cdn.shopify.com/s/files/1/0556/8086/0296/products/FlipperZero-angle_1000x.png", "desc": "Multi-tool Device for Geeks"},
    {"id": 2, "name": "Proxmark3 Rdv4", "price": "300 $", "image": "https://cdn.shopify.com/s/files/1/0006/8042/7638/products/proxmark3-rdv4-kit-main_1024x1024.jpg", "desc": "RFID Analysis Tool"},
    {"id": 3, "name": "Alfa Network Adapter", "price": "45 $", "image": "https://m.media-amazon.com/images/I/41-BS0r1+ML._AC_.jpg", "desc": "WiFi Monitor Mode Card"},
]

@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404
    # Notez que l'API par défaut pointe toujours vers un chemin relatif ou localhost
    # Mais l'étudiant devra changer ça pour scanner le réseau 192.168.0.X
    stock_api = f"/api/stock/{product_id}" 
    return render_template('product.html', product=product, stock_api=stock_api)

# --- VULNÉRABILITÉ SSRF ---

@app.route('/check-stock', methods=['POST'])
def check_stock():
    api_url = request.form.get('stockApi')
    if not api_url:
        return jsonify({"error": "Missing URL"}), 400

    # Si l'URL est relative (ex: /api/stock/1), on la complète
    if api_url.startswith('/'):
        api_url = f"http://localhost:5000{api_url}"

    parsed = urlparse(api_url)

    # --- SIMULATION DU RÉSEAU INTERNE (Le cœur du Lab) ---
    # Ici, on "fake" le comportement d'un réseau interne 192.168.0.X
    
    if parsed.hostname and parsed.hostname.startswith("192.168.0."):
        # Vérification du port (Le sujet demande le port 8080)
        if parsed.port != INTERNAL_PORT:
            return "Connection Refused (Port closed)", 500

        # Vérification de l'IP (Est-ce la bonne ?)
        if parsed.hostname == INTERNAL_HIDDEN_IP:
            # BINGO ! C'est la bonne machine
            
            # Gestion des routes de l'admin interne
            if parsed.path == "/admin":
                return render_template('admin_internal.html')
            
            elif parsed.path == "/admin/delete":
                user = ""
                if 'username' in api_url:
                    # Extraction basique du username
                    user = api_url.split('username=')[1].split('&')[0]
                
                if user == 'djamel':
                    return "✅ VICTORY: User 'Djamel Bensaber' deleted from Internal Backend System!"
                else:
                    return f"User '{user}' not found on internal system."
            
            else:
                return "404 Not Found (Internal Server)", 404
        else:
            # Mauvaise IP dans le range 192.168.0.X
            return f"Host {parsed.hostname} is unreachable (Timeout)", 500

    # --- COMPORTEMENT NORMAL (SSRF EXTERNE) ---
    try:
        # Permet de tester google.com pour valider le SSRF
        r = requests.get(api_url, timeout=1)
        return r.text
    except Exception as e:
        return f"Error fetching stock: {str(e)}", 500


# --- API STOCK PUBLIQUE ---
@app.route('/api/stock/<int:id>')
def public_stock(id):
    return "35 units in stock"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)