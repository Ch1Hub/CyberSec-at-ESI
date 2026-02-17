# 🛡️ SQL & NoSQL Injection Training Labs

Bienvenue dans la suite de laboratoires d'entraînement aux **Injections SQL et NoSQL**.  
Ce dépôt contient **24 environnements Dockerisés** simulant des vulnérabilités réelles, allant du niveau **débutant** au niveau **advanced (CTF)**.

---

## 📋 Instructions Générales

- **Catégorie :** Blackbox (Boîte Noire)
- **Objectif :** Exploiter l'application comme un attaquant externe.
- **Code Source :** 🚫 **INTERDIT**
  - Ne regardez pas le code (`app.py`) sauf si vous êtes totalement bloqué.
  - Le but est d’énumérer et comprendre le comportement de l’application.

---

## 🔒 Outils Automatisés

- **Labs 01 à 16 :** 🚫 **SQLMap INTERDIT**
  - Exploitation manuelle obligatoire (Burp Suite Repeater / Intruder).
  - Objectif : Comprendre la mécanique de la faille.

- **Labs 17 à 20 (SQL) :** ✅ **SQLMap AUTORISÉ**
  - Approche automatisée recommandée pour les bases volumineuses ou l'exfiltration massive.

- **Labs 21 à 24 (NoSQL) :** 🚫 **SQLMap INUTILE**
  - SQLMap ne fonctionne pas sur MongoDB.
  - ✅ **Scripts Python / Burp Suite** recommandés.

---

## 🚀 Démarrage d’un Lab

Chaque dossier contient son propre environnement isolé.

Exemple pour le Lab 01 :

    cd Lab01_HiddenData
    docker-compose up --build

Accédez ensuite à :  
`http://localhost:5000`

---

## 📚 Liste des Laboratoires

### 🔹 SQL Injection (Relational DB)

| #  | Titre                          | Type       | Difficulté | Description de la Mission |
|----|--------------------------------|------------|------------|----------------------------|
| 01 | Hidden Data Retrieval          | In-Band    | 🟢 Easy    | Modifier la clause WHERE pour afficher les produits cachés |
| 02 | Login Bypass                   | In-Band    | 🟢 Easy    | Se connecter en tant qu'admin sans connaître le mot de passe |
| 03 | UNION Attack (Col Count)       | In-Band    | 🟢 Easy    | Déterminer le nombre de colonnes renvoyées via UNION |
| 04 | UNION Text Finding             | In-Band    | 🟢 Easy    | Trouver quelle colonne accepte du texte |
| 05 | Retrieve Data via UNION        | In-Band    | 🟡 Medium  | Récupérer utilisateurs / mots de passe d'une autre table |
| 06 | Multi-Column Retrieval         | In-Band    | 🟡 Medium  | Concaténer plusieurs colonnes dans une cellule |
| 07 | DB Version (Oracle)            | In-Band    | 🟡 Medium  | Extraire la version de la base (Syntaxe Oracle) |
| 08 | DB Version (MySQL)             | In-Band    | 🟡 Medium  | Extraire la version de la base (Syntaxe MySQL) |
| 09 | Non-Oracle Schema              | In-Band    | 🟡 Medium  | Lister les tables via Information Schema |
| 10 | Oracle Schema Enumeration      | In-Band    | 🔴 Hard    | Lister les tables dans Oracle (Syntaxe spécifique) |
| 11 | Blind Boolean-Based            | Blind      | 🟡 Medium  | Deviner le mot de passe caractère par caractère (Vrai/Faux) |
| 12 | Visible Error-Based            | Error      | 🟡 Medium  | Forcer la base à divulguer des données via message d'erreur |
| 13 | Time-Based Blind               | Time       | 🟡 Medium  | Confirmer l'injection en faisant "dormir" la base |
| 14 | Time-Based Exfiltration        | Time       | 🔴 Hard    | Exfiltrer des données via mesure du temps de réponse |
| 15 | OOB Interaction (DNS)          | OOB        | 🔴 Hard    | Forcer la base à contacter un serveur externe (DNS/HTTP) |
| 16 | OOB Data Exfiltration          | OOB        | 🔥 Expert  | Exfiltrer des données via requête DNS vers serveur tiers |
| 17 | The Callback Trap              | OOB+Logic  | 🔥 Expert  | Scénario CTF : récupérer un token via OOB |
| 18 | Filter Evasion OOB             | OOB+WAF    | 🔥 Expert  | OOB avec contournement de filtres (espaces / mots-clés) |
| 19 | Header Injection               | Auto       | 🟡 Medium  | Injection via User-Agent (SQLMap recommandé) |
| 20 | Mass Extraction                | Auto       | 🔴 Hard    | Base volumineuse — extraction manuelle impossible |

### 🔹 NoSQL Injection (MongoDB)

| #  | Titre                          | Type       | Difficulté | Description de la Mission |
|----|--------------------------------|------------|------------|----------------------------|
| 21 | NoSQL Login Bypass             | NoSQLi     | 🟢 Easy    | Contourner l'authentification via opérateurs ($ne, $gt) |
| 22 | NoSQL Blind Extraction         | NoSQLi     | 🟡 Medium  | Exfiltration de données via Regex (Blind) |
| 23 | NoSQL Operator Injection       | NoSQLi     | 🟡 Medium  | Injection d'opérateurs pour altérer la logique JSON |
| 24 | SSJI (Server-Side JS)          | NoSQLi     | 🔴 Hard    | Injection de code JavaScript côté serveur ($where) |

---

## 🛠️ Outils Recommandés

- **Burp Suite Community / Pro** (Proxy, Repeater, Intruder)
- **Webhook.site** (Pour les labs OOB 15–18)
- **SQLMap** (Pour les labs SQL 19–20 uniquement)
- **Python** (Scripts `requests` indispensables pour NoSQLi et Time-Based)

---


# 🏴‍☠️ Happy Hacking!