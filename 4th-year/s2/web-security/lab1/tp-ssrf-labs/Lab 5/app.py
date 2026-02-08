from flask import Flask, request, render_template, redirect, jsonify
import requests
from urllib.parse import urlparse

app = Flask(__name__)

# --- CONFIGURATION CIBLE ---
INTERNAL_IP = "192.168.0.12"
INTERNAL_PORT = 8080
TARGET_USER = "DELLAA Abderrahmen"

# --- MOCK DATABASE ---
PRODUCTS = [
    {"id": 1, "name": "WiFi Pineapple", "price": "199 $", "image": "https://shop.hak5.org/cdn/shop/products/wifi-pineapple-mk7_530x@2x.jpg", "desc": "Automated WiFi Auditing"},
    {"id": 2, "name": "Shark Jack", "price": "59 $", "image": "https://shop.hak5.org/cdn/shop/products/shark-jack-cable_530x@2x.jpg", "desc": "Network Assessment Tool"},
    {"id": 3, "name": "Plunder Bug", "price": "39 $", "image": "https://shop.hak5.org/cdn/shop/products/plunder-bug_530x@2x.jpg", "desc": "Smart LAN Tap"},
]

@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404
    
    # URL par défaut : Un chemin relatif (Validé par le stock check)
    stock_api = f"/api/stock/{product_id}"
    
    # On calcule l'ID du produit suivant pour le lien "Next Product"
    next_id = product_id + 1 if product_id < 3 else 1
    next_path = f"/product/{next_id}"
    
    return render_template('product.html', product=product, stock_api=stock_api, next_path=next_path)

# --- VULNÉRABILITÉ 1 : OPEN REDIRECT ---

@app.route('/product/nextProduct')
def next_product():
    # Cette route prend un paramètre 'path' et redirige l'utilisateur dessus
    # SANS valider si c'est interne ou externe. C'est une faille Open Redirect.
    path = request.args.get('path')
    if not path:
        return "Missing path", 400
    return redirect(path)

# --- VULNÉRABILITÉ 2 : SSRF (Restricted) ---

@app.route('/check-stock', methods=['POST'])
def check_stock():
    api_url = request.form.get('stockApi')
    
    # 🛡️ DEFENSE : Validation stricte
    # Le checker n'accepte QUE les chemins relatifs (commençant par /)
    # Impossible de mettre http://192.168... directement.
    if not api_url or not api_url.startswith('/'):
        return "🚫 SECURITY BLOCK: Only local relative paths (starting with /) are allowed.", 400

    try:
        # Construction de l'URL locale complète
        # Ex: http://localhost:5000/product/nextProduct?path=...
        local_target = f"http://127.0.0.1:5000{api_url}"
        
        # 🚨 LA FAILLE : requests suit les redirections par défaut (allow_redirects=True)
        # Mais pour la simulation (car l'IP 192.168... n'existe pas vraiment sur le PC étudiant),
        # nous allons gérer la redirection manuellement pour "simuler" la connexion interne.
        
        # Etape 1 : On appelle l'URL locale sans suivre la redirection
        r = requests.get(local_target, allow_redirects=False, timeout=2)
        
        # Etape 2 : On regarde si c'est une redirection (302)
        if r.status_code == 302:
            redirect_location = r.headers.get('Location')
            
            # --- SIMULATION DU RÉSEAU INTERNE ---
            # Si la redirection pointe vers notre IP secrète
            if INTERNAL_IP in redirect_location and f":{INTERNAL_PORT}" in redirect_location:
                
                # Analyse de l'URL cible
                parsed = urlparse(redirect_location)
                
                if parsed.path == "/admin":
                    return render_template('admin_internal.html')
                
                elif parsed.path == "/admin/delete":
                     # Extraction du username
                    user = ""
                    if 'username=' in redirect_location:
                        user = redirect_location.split('username=')[1].split('&')[0]
                    
                    # Décodage URL simple (les espaces deviennent %20 parfois)
                    user = requests.utils.unquote(user)

                    if user == TARGET_USER:
                         return f"✅ VICTORY: User '{TARGET_USER}' deleted via Open Redirect Chain!"
                    return f"User '{user}' not found on internal system."
                
                return "404 Not Found (Internal)", 404

            # Si c'est une redirection vers autre chose (Google, etc.)
            try:
                # On essaie de la suivre (SSRF classique)
                r2 = requests.get(redirect_location, timeout=1)
                return r2.text
            except:
                return f"Redirected to {redirect_location}, but could not connect."

        return r.text

    except Exception as e:
        return f"Error: {str(e)}", 500

# --- API STOCK PUBLIQUE ---
@app.route('/api/stock/<int:id>')
def public_stock(id):
    return "50 units available"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)