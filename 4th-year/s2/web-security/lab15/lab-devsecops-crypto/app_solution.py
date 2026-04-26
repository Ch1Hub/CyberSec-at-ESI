from flask import Flask, request, jsonify
import os
import sys
import binascii
import hvac

# Imports Sécurité (Modernes)
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

app = Flask(__name__)

# ==========================================
# 1. CONFIGURATION VAULT (TP 14 - Phase 5)
# ==========================================
# Remarque : En production, ces IDs seraient passés via variables d'environnement
VAULT_URL = os.getenv('VAULT_ADDR', 'http://127.0.0.1:8200')
ROLE_ID = os.getenv('VAULT_ROLE_ID')
SECRET_ID = os.getenv('VAULT_SECRET_ID')

try:
    client = hvac.Client(url=VAULT_URL)
    
    # Authentification via AppRole
    client.auth.approle.login(
        role_id=ROLE_ID,
        secret_id=SECRET_ID
    )

    if not client.is_authenticated():
        raise Exception("Authentification Vault échouée")

    # Lecture dynamique de la clé secrète
    vault_response = client.secrets.kv.v2.read_secret_version(path='myapp')
    extracted_key = vault_response['data']['data']['crypto_key']
    
    # La clé doit faire 16, 24 ou 32 octets pour AES
    SECRET_KEY = extracted_key.encode()

except Exception as e:
    print(f"ERREUR CRITIQUE : Impossible de récupérer la clé dans Vault : {e}")
    sys.exit(1)


# ==========================================
# 2. GESTION DES IDENTITÉS (TP 15 - Phase 1 & 3)
# ==========================================
ph = PasswordHasher()

@app.route('/register', methods=['POST'])
def register():
    password = request.json.get('password', '')
    if not password:
        return jsonify({"error": "Password required"}), 400
    
    # Sécurisé : Argon2id (Hachage lent + Sel automatique)
    hashed_password = ph.hash(password)
    
    return jsonify({
        "status": "User created", 
        "hash": hashed_password
    })

@app.route('/login', methods=['POST'])
def login():
    provided_hash = request.json.get('hash', '')
    password = request.json.get('password', '')
    
    try:
        # Vérification sécurisée contre les attaques temporelles
        ph.verify(provided_hash, password)
        return jsonify({"status": "Login successful!"})
    except VerifyMismatchError:
        return jsonify({"status": "Access Denied"}), 401
    except Exception:
        return jsonify({"status": "Invalid format"}), 400


# ==========================================
# 3. CHIFFREMENT DES DONNÉES (TP 15 - Phase 2 & 4)
# ==========================================

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json.get('data', '').encode()
    if not data:
        return jsonify({"error": "No data to encrypt"}), 400

    # Sécurisé : AES-GCM (Authentifié + Nonce unique)
    aesgcm = AESGCM(SECRET_KEY)
    nonce = os.urandom(12)  # Nonce standard de 96 bits
    
    ciphertext = aesgcm.encrypt(nonce, data, None)
    
    # On concatène Nonce + Ciphertext pour pouvoir déchiffrer plus tard
    final_payload = nonce + ciphertext
    
    return jsonify({
        "status": "Data encrypted", 
        "ciphertext": binascii.hexlify(final_payload).decode()
    })

@app.route('/decrypt', methods=['POST'])
def decrypt():
    payload_hex = request.json.get('ciphertext', '')
    
    try:
        payload_bytes = binascii.unhexlify(payload_hex)
        
        # Extraction des composants
        nonce = payload_bytes[:12]
        encrypted_data = payload_bytes[12:]
        
        aesgcm = AESGCM(SECRET_KEY)
        # Déchiffrement + Vérification de l'intégrité (Tag)
        decrypted_data = aesgcm.decrypt(nonce, encrypted_data, None)
        
        return jsonify({
            "status": "Data decrypted", 
            "plaintext": decrypted_data.decode()
        })
    except Exception as e:
        # En cas de modification du ciphertext, GCM lèvera une erreur d'intégrité
        return jsonify({
            "status": "Decryption failed (Integrity error)", 
            "error": "Invalid token or modified data"
        }), 400

if __name__ == '__main__':
    # Rappel : host='0.0.0.0' est nécessaire pour l'accès via Docker
    app.run(debug=True, host='0.0.0.0', port=5000)