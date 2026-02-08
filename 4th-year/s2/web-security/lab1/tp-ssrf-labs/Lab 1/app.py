from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# --- MOCK DATABASE ---
PRODUCTS = [
    {"id": 1, "name": "HackRF One", "price": "300 $", "image": "https://m.media-amazon.com/images/I/61bfXyQ+cNL._AC_SL1000_.jpg", "desc": "SDR Radio for Pentesting"},
    {"id": 2, "name": "Rubber Ducky", "price": "49 $", "image": "https://shop.hak5.org/cdn/shop/products/usb-rubber-ducky-deluxe_530x@2x.jpg", "desc": "Keystroke Injection Tool"},
    {"id": 3, "name": "WiFi Pineapple", "price": "199 $", "image": "https://shop.hak5.org/cdn/shop/products/wifi-pineapple-mk7_530x@2x.jpg", "desc": "Rogue Access Point"},
]

@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404
    # URL interne par défaut
    stock_api = f"http://localhost:5000/api/internal/stock/{product_id}"
    return render_template('product.html', product=product, stock_api=stock_api)

@app.route('/check-stock', methods=['POST'])
def check_stock():
    api_url = request.form.get('stockApi')
    if not api_url:
        return jsonify({"error": "Missing URL"}), 400
    try:
        # 🚨 LA FAILLE EST ICI
        r = requests.get(api_url, timeout=2)
        return r.text
    except Exception as e:
        return f"Error connecting to backend: {str(e)}", 500

@app.route('/api/internal/stock/<int:id>')
def internal_stock(id):
    return "99 units available"

@app.route('/admin')
def admin_panel():
    # Protection Localhost
    if request.remote_addr != '127.0.0.1':
        return render_template('admin.html', content="⛔ ACCESS DENIED: Admin panel is restricted to Localhost IP."), 403
    
    return render_template('admin.html', content="🔓 WELCOME ADMIN", is_admin=True)

@app.route('/admin/delete')
def delete_user():
    if request.remote_addr != '127.0.0.1':
        return "⛔ Access Denied", 403
        
    username = request.args.get('username')
    # Modification ici pour cibler Djamel
    if username == 'djamel':
        return "✅ SUCCESS: User 'Djamel Bensaber' has been deleted from the database."
    return f"User '{username}' not found.", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)