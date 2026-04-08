# 🛡️ Workshop No. 11: Enterprise IAM & Secure OIDC Implementation

### ESI-SBA Cybersecurity Training Labs

Transitioning from offensive security (breaking) to defensive architecture (building), this workshop focuses on implementing a secure Identity and Access Management (IAM) stack.

Using **Keycloak**, **OpenLDAP**, and a **Python Flask** application, you will act as a Security Architect to build a robust Single Sign-On (SSO) environment. You will federate identities, map legacy LDAP attributes to modern OIDC claims, and enforce the secure Authorization Code Flow while mitigating the vulnerabilities explored in previous labs.

---

## 🏗️ Architecture Overview

This laboratory deploys a modern microservices identity architecture using three interconnected containers:

1. **OpenLDAP (Corporate Directory):** The legacy database pre-populated with organizational units and employee records.
2. **Keycloak (Identity Provider / IdP):** The centralized authorization server managing security realms, federation, and OIDC token issuance.
3. **Internal Application (Flask):** The service provider (backend application) that currently lacks authentication and must be secured.

---

## 🚀 Quick Start Guide

Ensure Docker and Docker Compose are installed on your machine. To avoid network congestion during the lab, it is highly recommended to pull the images in advance.

1. **Navigate to the workshop directory:**
   ```bash
   cd Workshop11_IAM_Implementation
   ```
