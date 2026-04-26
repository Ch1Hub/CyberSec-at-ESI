from flask import Flask, request, jsonify
import hashlib
import binascii
from Crypto.Cipher import AES  # Requires: pip install pycryptodome
from Crypto.Util.Padding import pad

app = Flask(__name__)

# STATIC HARDCODED KEY - A MAJOR VULNERABILITY
SECRET_KEY = b'1234567890123456' 

@app.route('/register', methods=['POST'])
def register():
    password = request.json.get('password', '')
    # VULNERABLE: MD5 is fast and unsalted. Prone to Rainbow Table attacks.
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    return jsonify({"status": "User created", "hash": hashed_password})

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json.get('data', '')
    # VULNERABLE: ECB mode leaks patterns in data.
    # Manual padding is required, introducing padding oracle risks.
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    padded_data = pad(data.encode(), 16)
    ciphertext = cipher.encrypt(padded_data)
    
    return jsonify({
        "status": "Data encrypted", 
        "ciphertext": binascii.hexlify(ciphertext).decode()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)