from flask import Flask, request, render_template, jsonify
from urllib.parse import unquote
import requests

app = Flask(__name__)

# --- CIBLE DU LAB ---
TARGET_USER = "DELLAA Abderrahmen"
ALLOWED_HOST = "stock.shop-internal.net"

# --- MOCK DATABASE ---
PRODUCTS = [
    {"id": 1, "name": "O.MG Cable", "price": "120 $", "image": "https://shop.hak5.org/cdn/shop/products/omg_cable_keylogger_530x@2x.jpg", "desc": "Looks like a cable, acts like a keyboard."},
    {"id": 2, "name": "Lan Turtle", "price": "60 $", "image": "https://shop.hak5.org/cdn/shop/products/lan-turtle-sd_530x@2x.jpg", "desc": "Covert System Administration Tool."},
    {"id": 3, "name": "USB Rubber Ducky", "price": "80 $", "image": "https://shop.hak5.org/cdn/shop/products/usb-rubber-ducky-deluxe_530x@2x.jpg", "desc": "The Original Keystroke Injection Tool."},
]

@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404
    # URL qui respecte la whitelist par défaut
    stock_api = f"http://{ALLOWED_HOST}/api/stock/{product_id}"
    return render_template('product.html', product=product, stock_api=stock_api)

# --- VULNÉRABILITÉ EXPERT (Whitelist Bypass) ---

@app.route('/check-stock', methods=['POST'])
def check_stock():
    api_url = request.form.get('stockApi')
    if not api_url:
        return jsonify({"error": "Missing URL"}), 400

    # 🛡️ DEFENSE : WHITELIST RIGOUREUSE (Apparemment...)
    # Le développeur exige que le nom de domaine autorisé soit présent dans l'URL.
    # C'est une vérification commune mais faible si on utilise des regex ou 'in'.
    if ALLOWED_HOST not in api_url:
        return f"🚫 SECURITY ALERT: External hosts are blocked. You must use {ALLOWED_HOST}", 400

    try:
        # 🚨 LA FAILLE DE LOGIQUE (EXPERT)
        # Flask a déjà décodé l'URL une première fois (%2523 -> %23).
        # Simulation d'un backend qui décode l'URL (urldecode) avant de l'utiliser.
        # Cela transforme le %23 en '#' (fragment anchor).
        
        decoded_url = unquote(api_url)

        # DEBUG: Pour montrer aux étudiants ce qui se passe dans le serveur
        print(f"[SERVER LOG] Original: {api_url}")
        print(f"[SERVER LOG] Decoded : {decoded_url}")

        # Lors de l'envoi :
        # Si decoded_url est : http://localhost:80#@stock.shop-internal.net/...
        # La librairie 'requests' voit le '#' et S'ARRÊTE LÀ pour la connexion TCP.
        # Elle se connecte donc à localhost:80.
        # La partie '@stock...' est considérée comme un commentaire/fragment local.
        
        r = requests.get(decoded_url, timeout=2)
        return r.text

    except requests.exceptions.ConnectionError:
        return "Error: Failed to connect to backend system.", 500
    except Exception as e:
        return f"Internal Error: {str(e)}", 500

# --- L'ADMINISTRATION (Cible) ---

@app.route('/admin')
def admin_panel():
    # Protection Localhost
    if request.remote_addr != '127.0.0.1':
        return render_template('admin.html', content="⛔ ACCESS DENIED: Internal use only."), 403
    
    return render_template('admin.html', content="🔓 WELCOME ADMIN", is_admin=True)

@app.route('/admin/delete')
def delete_user():
    if request.remote_addr != '127.0.0.1':
        return "⛔ Access Denied", 403
        
    username = request.args.get('username')
    
    # Vérification exacte du nom (Case sensitive et espaces)
    if username == TARGET_USER:
        return f"✅ EXPERT VICTORY: User '{TARGET_USER}' has been deleted!"
    
    return f"User '{username}' not found. (Did you copy the name exactly?)", 404

if __name__ == '__main__':
    # Hack pour autoriser le caractère '#' dans les requêtes brutes si nécessaire
    app.run(host='0.0.0.0', port=5000)