# Lab : Advanced Blind SSRF & OOB Exfiltration

**Module :** Sécurité Web Avancée  
**Niveau :** Difficile (Hard)  
**Type :** Black Box / Grey Box

---

## 🏗️ Installation & Lancement

Ce laboratoire utilise **Docker** pour simuler une architecture micro-services réaliste.

### Prérequis

- Docker Desktop (ou Docker Engine sur Linux)
- Docker Compose

### Démarrage

1.  Ouvrez un terminal dans le dossier du projet.
2.  Lancez l'environnement :
    ```bash
    docker-compose up --build
    ```
3.  Accédez à l'application "Webhook Tester" via votre navigateur :
    - **URL :** `http://localhost:5000`

---

## ⚔️ Scénario (Mission)

Vous auditez une application interne nommée **"Webhook Connectivity Tester"**. Cet outil permet aux développeurs de vérifier si leurs APIs sont joignables depuis l'infrastructure de l'entreprise.

Cependant, des rumeurs indiquent qu'un **panneau d'administration caché** (Internal Admin Panel) est hébergé sur le même réseau interne que l'application, mais il n'est pas accessible directement depuis l'extérieur.

Ce panneau d'administration contient un **FLAG secret** unique, généré aléatoirement au démarrage du serveur.

### Votre Objectif

Vous devez récupérer le contenu du fichier `/flag.txt` situé sur le serveur d'administration interne.

**Format du Flag :** `ESI-SBA{...}`

---

## 🕵️‍♂️ Indices & Informations Techniques

Comme vous êtes dans un scénario "Blind" (Aveugle), l'application ne vous affichera jamais le contenu des réponses HTTP internes. Vous devez déduire ce qui se passe autrement.

1.  **Architecture Réseau :**
    - L'application publique tourne sur un conteneur.
    - Le réseau interne Docker est : `172.20.0.0/24`.
    - L'application publique filtre les accès vers `localhost` (127.0.0.1), mais peut-être pas vers les autres machines du réseau...

2.  **La Cible (Admin Panel) :**
    - Elle se trouve quelque part sur le réseau `172.20.0.x`.
    - L'application ne répond pas aux requêtes GET classiques à la racine.
    - **Indice Critique :** Les développeurs utilisent souvent un endpoint nommé `/admin/forward_flag` qui accepte un paramètre `dest` (destination) pour envoyer des logs ou des secrets vers un serveur tiers.

3.  **Méthodologie recommandée :**
    - **Étape 1 :** Confirmer la vulnérabilité SSRF (Time-Based).
    - **Étape 2 :** Scanner le réseau interne pour trouver l'IP du service Admin (Time-Based ou Error-Based).
    - **Étape 3 :** Exploiter la fonctionnalité de "rebond" (Out-of-Band) pour forcer le serveur Admin à vous envoyer le flag sur votre propre machine (ou via un outil comme _webhook.site_).

---

## 🚫 Règles

1.  **Ne pas modifier le code source :** L'objectif est d'attaquer l'application comme un pentester externe.
2.  **Outils autorisés :** Burp Suite, Zap Proxy, Netcat, Python, Webhook.site.

---

## 📝 Livrables

Pour valider ce TP, vous devez soumettre un petit rapport (PDF ou Markdown) contenant :

1.  La preuve de la détection de l'IP interne (ex: capture d'écran des temps de réponse).
2.  Le payload final utilisé pour l'exfiltration.
3.  **La valeur exacte du FLAG** que vous avez reçu (ex: `ESI-SBA{OOB_MASTER_x9s8d7}`).
