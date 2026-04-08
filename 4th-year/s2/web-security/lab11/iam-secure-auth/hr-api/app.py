from flask import Flask, request, jsonify
import jwt
from jwt import PyJWKClient

app = Flask(__name__)

# Keycloak JWKS endpoint to fetch public keys for JWT signature verification
JWKS_URL = "http://keycloak:8080/realms/ESI-Corporate/protocol/openid-connect/certs"
jwks_client = PyJWKClient(JWKS_URL)

def verify_token(token):
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        data = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False} # Simplified for lab environment
        )
        return data
    except Exception as e:
        print(f"Token validation error: {e}")
        return None

@app.route('/api/salary', methods=['GET'])
def get_salary():
    """Endpoint protected for human users (Delegated Access)"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid token format'}), 401

    token = auth_header.split(' ')[1]
    payload = verify_token(token)

    if not payload or 'preferred_username' not in payload:
        return jsonify({'error': 'Unauthorized. User token required.'}), 403

    return jsonify({'employee': payload['preferred_username'], 'salary': '120,000 DZD'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Endpoint protected for automated scripts (Machine-to-Machine)"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid token format'}), 401

    token = auth_header.split(' ')[1]
    payload = verify_token(token)

    # Machine tokens typically do not have a preferred_username, but possess a clientId (azp)
    client_id = payload.get('clientId') or payload.get('azp')
    
    if not payload or client_id != 'hr-cron-job':
        return jsonify({'error': 'Forbidden. Specialized machine token required.'}), 403

    return jsonify({'total_employees': 42, 'average_salary': '105,000 DZD'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)