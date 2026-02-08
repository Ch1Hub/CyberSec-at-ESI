from flask import Flask, request, render_template, jsonify
from urllib.parse import urlparse, unquote
import requests

app = Flask(__name__)

# --- MOCK DATABASE ---
PRODUCTS = [
    {"id": 1, "name": "Bash Bunny", "price": "120 $", "image": "https://shop.hak5.org/cdn/shop/products/bash-bunny_530x@2x.jpg", "desc": "USB Attack Platform"},
    {"id": 2, "name": "Key Croc", "price": "150 $", "image": "https://shop.hak5.org/cdn/shop/products/key-croc_530x@2x.jpg", "desc": "Keylogger Implant"},
    {"id": 3, "name": "Screen Crab", "price": "180 $", "image": "https://shop.hak5.org/cdn/shop/products/screen-crab_530x@2x.jpg", "desc": "HDMI Man-in-the-Middle"},
]

@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404
    # URL par défaut
    stock_api = f"http://stock.shop-internal.net/api/stock/{product_id}"
    return render_template('product.html', product=product, stock_api=stock_api)

# --- VULNÉRABILITÉ SSRF AVEC FILTRES ---

@app.route('/check-stock', methods=['POST'])
def check_stock():
    api_url = request.form.get('stockApi')
    if not api_url:
        return jsonify({"error": "Missing URL"}), 400

    # 🛡️ DEFENSE 1 : BLACKLIST IP/HOST
    # Le développeur bloque naivement '127.0.0.1' et 'localhost'
    parsed = urlparse(api_url)
    hostname = parsed.hostname

    if hostname in ['127.0.0.1', 'localhost']:
        return "🚫 SECURITY ALERT: Access to localhost/127.0.0.1 is strictly forbidden!", 400

    # 🛡️ DEFENSE 2 : BLACKLIST MOT-CLÉ
    # Le développeur bloque le mot "admin" pour empêcher l'accès au panneau
    # Note: request.form a déjà décodé l'URL une fois (ex: %2561 devient %61)
    if 'admin' in api_url:
        return "🚫 SECURITY ALERT: The term 'admin' is blocked in URLs.", 400

    # --- EXECUTION DE LA REQUÊTE ---
    try:
        # 🚨 LA FAILLE : requests est permissif
        # 1. Il accepte '127.1' comme étant '127.0.0.1' (Bypass Filtre 1)
        # 2. Si on envoie '%61dmin' (qui vient du double encodage), 
        #    le filtre 'admin' ne matche pas, mais le serveur de destination comprendra 'admin'.
        r = requests.get(api_url, timeout=2)
        return r.text
    except Exception as e:
        return f"Error fetching stock: {str(e)}", 500

# --- L'ADMINISTRATION (Cible) ---

@app.route('/admin')
def admin_panel():
    # Protection standard : Localhost seulement
    if request.remote_addr != '127.0.0.1':
        return render_template('admin.html', content="⛔ ACCESS DENIED: Localhost only."), 403
    
    return render_template('admin.html', content="🔓 WELCOME ADMIN", is_admin=True)

@app.route('/admin/delete')
def delete_user():
    if request.remote_addr != '127.0.0.1':
        return "⛔ Access Denied", 403
        
    username = request.args.get('username')
    if username == 'djamel':
        return "✅ VICTORY: User 'Djamel Bensaber' has been deleted! (Filter Bypassed)"
    return f"User '{username}' not found.", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)