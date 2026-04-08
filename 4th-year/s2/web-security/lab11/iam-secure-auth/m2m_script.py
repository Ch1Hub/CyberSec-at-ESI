import requests

# Security Architect Exercise: Implement the Client Credentials Flow
TOKEN_ENDPOINT = "http://localhost:8080/realms/ESI-Corporate/protocol/openid-connect/token"
API_ENDPOINT = "http://localhost:5001/api/stats"

CLIENT_ID = "hr-cron-job"
# 🛠️ EXERCISE: Insert the secret generated from the Keycloak Admin Console
CLIENT_SECRET = "REDACTED_KEYCLOAK_CLIENT_SECRET"

print("[*] Initiating Machine-to-Machine Authentication...")

payload = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}

# 1. Requesting the Access Token from the Identity Provider
auth_response = requests.post(TOKEN_ENDPOINT, data=payload)

if auth_response.status_code == 200:
    access_token = auth_response.json().get("access_token")
    print("[+] OAuth 2.0 Access Token Acquired successfully.\n")
    
    # 2. Querying the Protected Resource Server
    print("[*] Interrogating Resource Server (HR API)...")
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    api_response = requests.get(API_ENDPOINT, headers=headers)
    
    if api_response.status_code == 200:
        print("[+] Resource Server Authorization Granted. Data retrieved:")
        print(api_response.json())
    else:
        print(f"[-] Resource Server Authorization Denied. HTTP {api_response.status_code}")
        print(api_response.text)
else:
    print("[-] Identity Provider Authentication Failed.")
    print(auth_response.text)
