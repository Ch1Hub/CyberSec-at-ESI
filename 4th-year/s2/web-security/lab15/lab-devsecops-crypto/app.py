from flask import Flask, request, jsonify
import os
import sys
import binascii
import hvac
from hvac.exceptions import Forbidden, InvalidPath, InvalidRequest, VaultError
from argon2 import PasswordHasher
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

app = Flask(__name__)

VAULT_URL = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
ROLE_ID = os.getenv("VAULT_ROLE_ID")
SECRET_ID = os.getenv("VAULT_SECRET_ID")


def load_key_from_vault() -> bytes:
    if not ROLE_ID or not SECRET_ID:
        raise RuntimeError("VAULT_ROLE_ID and VAULT_SECRET_ID are required")

    client = hvac.Client(url=VAULT_URL)
    client.auth.approle.login(role_id=ROLE_ID, secret_id=SECRET_ID)

    if not client.is_authenticated():
        raise RuntimeError("Vault authentication failed")

    secret = client.secrets.kv.v2.read_secret_version(
        path="myapp",
        raise_on_deleted_version=True,
    )
    crypto_key = secret["data"]["data"]["crypto_key"]

    if not isinstance(crypto_key, str):
        raise RuntimeError("Vault crypto_key must be a string")

    key_bytes = crypto_key.encode("utf-8")
    if len(key_bytes) not in (16, 24, 32):
        raise RuntimeError("Vault crypto_key must be 16, 24, or 32 bytes")

    return key_bytes


try:
    SECRET_KEY = load_key_from_vault()
except (Forbidden, InvalidPath, InvalidRequest, KeyError, RuntimeError, VaultError) as exc:
    print(f"Critical error: unable to load key from Vault: {exc}", file=sys.stderr)
    sys.exit(1)


password_hasher = PasswordHasher()

@app.route('/register', methods=['POST'])
def register():
    payload = request.get_json(silent=True) or {}
    password = payload.get("password")

    if not isinstance(password, str) or not password:
        return jsonify({"error": "Password required"}), 400

    hashed_password = password_hasher.hash(password)
    return jsonify({"status": "User created", "hash": hashed_password})


@app.route('/encrypt', methods=['POST'])
def encrypt():
    payload = request.get_json(silent=True) or {}
    data = payload.get("data")

    if not isinstance(data, str) or not data:
        return jsonify({"error": "No data to encrypt"}), 400

    aesgcm = AESGCM(SECRET_KEY)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data.encode("utf-8"), None)
    final_payload = nonce + ciphertext

    return jsonify({
        "status": "Data encrypted",
        "ciphertext": binascii.hexlify(final_payload).decode("ascii")
    })

if __name__ == '__main__':
    app.run(
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
        host=os.getenv("FLASK_HOST", "127.0.0.1"),
        port=int(os.getenv("FLASK_PORT", "5000")),
    )
