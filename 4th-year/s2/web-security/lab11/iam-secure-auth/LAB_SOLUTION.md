# 🎓 Lab 11 Solution - IAM & Secure OIDC Implementation

## ✅ Completed Configuration

### 1. **Keycloak Setup**
- **Realm**: `ESI-Corporate`
- **Admin Console**: http://localhost:8080
  - Username: `admin`
  - Password: `admin`

### 2. **LDAP Federation**
- **Provider**: OpenLDAP
- **Configuration**:
  ```
  Connection URL: ldap://openldap:389
  Users DN: ou=users,dc=esi-sba,dc=dz
  Bind DN: cn=admin,dc=esi-sba,dc=dz
  Bind Credential: REDACTED_LDAP_ADMIN_PASSWORD
  Username LDAP attribute: uid
  RDN LDAP attribute: cn
  ```
- **Custom Mapper**: `department-mapper`
  - Maps: `employeeType` (LDAP) → `department` (Keycloak)

### 3. **LDAP Users**
Users were loaded manually into OpenLDAP:
```bash
# User: djamel
Username: djamel
Password: password123
Email: djamel@esi-sba.dz
Department: CyberSecurity
```

### 4. **OAuth 2.0 Clients**

#### Client 1: `internal-webapp` (Authorization Code Flow)
- **Client Type**: Confidential
- **Authentication Flow**: Standard flow (Authorization Code)
- **Redirect URI**: `http://localhost:5000/auth`
- **Client Secret**: `REDACTED_KEYCLOAK_CLIENT_SECRET`
- **Purpose**: User login for web application

#### Client 2: `hr-cron-job` (Client Credentials Flow)
- **Client Type**: Confidential
- **Authentication Flow**: Service accounts roles
- **Client Secret**: `REDACTED_KEYCLOAK_CLIENT_SECRET`
- **Purpose**: Machine-to-machine API access

### 5. **Custom Claims Configuration**
- Added `department` claim to `internal-webapp-dedicated` scope
- Claim is included in: ID token, Access token, UserInfo endpoint

### 6. **Docker Networking Fix**
- Added `extra_hosts: localhost:host-gateway` to web-app service
- Changed CONF_URL to use `localhost:8080` instead of `keycloak:8080`
- This allows browser to access Keycloak while container can reach it via host gateway

---

## 🧪 Testing

### Test 1: Web Application Login
```bash
# Open browser
http://localhost:5000

# Click "Login via ESI SSO"
# Credentials: djamel / password123
# ✅ Success: User info displayed with department claim
```

### Test 2: Machine-to-Machine Authentication
```bash
# Run M2M script
python3 m2m_script.py

# ✅ Success: Retrieved HR statistics from protected API
```

---

## 🔑 Key Concepts Learned

1. **OIDC/OAuth 2.0 Flows**
   - Authorization Code Flow (user login)
   - Client Credentials Flow (M2M)

2. **Identity Federation**
   - Connected legacy LDAP to modern IdP
   - Attribute mapping (LDAP → Token claims)

3. **JWT Token Validation**
   - HR API validates tokens using JWKS
   - Different endpoints for user vs machine tokens

4. **Docker Networking**
   - Container-to-container communication
   - Host gateway for browser access

---

## 📦 Services & Endpoints

| Service | Port | Purpose |
|---------|------|---------|
| Keycloak | 8080 | Identity Provider |
| OpenLDAP | 389 | Corporate Directory |
| Web App | 5000 | Internal Application |
| HR API | 5001 | Protected Resource Server |

---

## 🎯 Architecture Flow

```
User Browser → Web App (5000) → Keycloak (8080) → LDAP (389)
                                      ↓
                                  ID Token
                                      ↓
                              Web App Session

Cron Script → Keycloak (8080) → Access Token → HR API (5001)
```

---

## 🚀 Quick Start (After Restart)

```bash
# Start all services
docker compose up -d

# Load LDAP user (if needed)
docker exec -i esi-ldap ldapadd -x -D "cn=admin,dc=esi-sba,dc=dz" -w REDACTED_LDAP_ADMIN_PASSWORD <<EOF
dn: ou=users,dc=esi-sba,dc=dz
objectClass: organizationalUnit
ou: users
EOF

docker exec -i esi-ldap ldapadd -x -D "cn=admin,dc=esi-sba,dc=dz" -w REDACTED_LDAP_ADMIN_PASSWORD <<EOF
dn: cn=djamel,ou=users,dc=esi-sba,dc=dz
objectClass: inetOrgPerson
cn: djamel
sn: cyberdz
uid: djamel
userPassword: password123
mail: djamel@esi-sba.dz
employeeType: CyberSecurity
EOF

# Test web login
# Browser: http://localhost:5000

# Test M2M
python3 m2m_script.py
```

---

**Lab completed successfully! ✅**
