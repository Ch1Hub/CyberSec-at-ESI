# TP SSRF (LAB 2) : Attaque sur Backend Distant

**ESI SBA - 04ème année Cys**

## 🎯 Objectif

Dans ce scénario, l'interface d'administration n'est pas hébergée sur le serveur web lui-même (`localhost`), mais sur un **autre serveur** situé dans le réseau interne de l'entreprise.

**Informations connues :**

- Plage IP du réseau interne : `192.168.0.0/24` (de .1 à .255)
- Port de l'administration : `8080`
- Chemin de l'administration : `/admin`

Votre but est de scanner le réseau pour trouver l'adresse IP active, puis de supprimer l'utilisateur **Djamel Bensaber**.