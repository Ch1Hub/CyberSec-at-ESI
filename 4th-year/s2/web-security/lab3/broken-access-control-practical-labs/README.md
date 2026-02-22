# 🛡️ Broken Access Control (BAC) Training Labs

Bienvenue dans la suite de laboratoires d'entraînement dédiés aux vulnérabilités de **Contrôle d'Accès Défaillant (Broken Access Control)**.

Ce dépôt contient **13 environnements Dockerisés (Labs 01 à 13)** simulant des failles de conception réelles, allant du niveau **débutant (Apprentice)** au niveau **avancé (Practitioner)**.

---

## 📋 Instructions Générales

- **Catégorie :** Blackbox (Boîte Noire)
- **Objectif :**
  - 🔼 Élever vos privilèges (**Vertical Privilege Escalation**)
  - 🔓 Accéder aux données d'autres utilisateurs (**Horizontal Access Control Bypass**)

- **Code Source :** 🚫 **INTERDIT**
  - Ne regardez pas le code (`app.py`) sauf si vous êtes totalement bloqué.
  - Le but est d’énumérer, d’intercepter et de manipuler les requêtes HTTP.

---

## 🔒 Outils Automatisés

- **Scanners de vulnérabilités :** 🚫 **INTERDITS**
  - (Nessus, ZAP auto-scan, etc.)
  - L'exploitation de ces failles nécessite une analyse logique du comportement de l'application.

- **Approche manuelle obligatoire :** ✅
  - Burp Suite (Proxy, Repeater)
  - Browser Developer Tools

---

## 🚀 Démarrage d’un Lab

Chaque dossier contient son propre environnement isolé.

### Exemple – Lab 01

```bash
cd Lab01_Unprotected_Admin
docker-compose up --build
```

Accédez ensuite à l’application via :

```
http://localhost:5000
```

---

# 📚 Liste des Laboratoires

## 🔹 Broken Access Control (BAC) & IDOR

| #   | Titre                          | Type                | Difficulté | Description de la Mission                                                                                               |
| --- | ------------------------------ | ------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------- |
| 01  | Unprotected Admin (robots.txt) | URL Leakage         | 🟢 Easy    | Inspecter le fichier `robots.txt` pour découvrir l'URL secrète du panel d'administration et supprimer un utilisateur.   |
| 02  | Unpredictable Admin URL        | JS Code Leakage     | 🟢 Easy    | Trouver l'URL d'administration cachée dans le code source (JavaScript) pour supprimer un utilisateur.                   |
| 03  | User-Controlled Role           | Cookie Manipulation | 🟢 Easy    | Modifier un cookie d'autorisation stocké en clair pour élever ses privilèges au rang d'admin.                           |
| 04  | Mass Assignment                | API / JSON          | 🟡 Medium  | Injecter un champ inattendu (`roleid`) dans un payload JSON pour s'auto-promouvoir lors d'une mise à jour de profil.    |
| 05  | Basic IDOR                     | IDOR                | 🟢 Easy    | Manipuler un paramètre d'URL (`?id=`) pour accéder au profil d'un autre utilisateur et voler sa clé API.                |
| 06  | IDOR with Unpredictable IDs    | IDOR + Data Leakage | 🟡 Medium  | Trouver l'UUID (non devinable) de la cible via une fuite d'information pour exploiter un IDOR.                          |
| 07  | Data Leakage in Redirect       | Info Disclosure     | 🟡 Medium  | Intercepter une réponse de redirection (HTTP 302) contenant encore des données sensibles dans son body HTML.            |
| 08  | IDOR to Password Leak          | IDOR                | 🟡 Medium  | Accéder au profil de l'administrateur via IDOR et inspecter le code source pour lire son mot de passe pré-rempli.       |
| 09  | Static File IDOR               | IDOR                | 🟡 Medium  | Télécharger des historiques de chat appartenant à d'autres utilisateurs via des noms de fichiers prévisibles (`1.txt`). |
| 10  | Proxy/WAF Desynchronization    | Header Manipulation | 🔴 Hard    | Contourner un proxy bloquant `/admin` en utilisant le header non standard `X-Original-URL`.                             |
| 11  | Method-based Circumvention     | HTTP Method Flaw    | 🔴 Hard    | Contourner une restriction d'accès ciblant la méthode `POST` en forgeant une requête `GET` ou `POSTX`.                  |
| 12  | Multi-step Process Bypass      | Logic Flaw          | 🔴 Hard    | Forger directement la requête de l'étape finale d'un processus sans passer par l'étape de validation protégée.          |
| 13  | Referer-based Access Control   | Header Spoofing     | 🔴 Hard    | Usurper l'en-tête HTTP `Referer` pour tromper le backend et prouver que la requête vient du panel admin.                |

---

# 🛠️ Outils Recommandés

- **Burp Suite Community**
  - Intercepter les requêtes HTTP
  - Modifier les headers
  - Manipuler les payloads JSON
  - Capturer et analyser les redirections 302

- **Browser Developer Tools (F12)**
  - Inspecteur d’éléments
  - Console JavaScript
  - Onglet Network

- **Éditeur de texte / Décodeur**
  - Analyse des cookies
  - Décodage Base64
  - Inspection des données interceptées

---

# 🏴‍☠️ Happy Hacking!
