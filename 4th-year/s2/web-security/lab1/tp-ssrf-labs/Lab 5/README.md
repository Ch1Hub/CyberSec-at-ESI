# TP SSRF (LAB 5) : Bypass via Open Redirect
**ESI SBA CyberLab**

## 🎯 Objectif
Le "Stock Checker" a été sécurisé. Il refuse catégoriquement toute URL qui ne commence pas par `/` (chemin local). Impossible de scanner le réseau externe ou interne directement.

Cependant, l'application contient une autre vulnérabilité : une **Open Redirection**.

**Données cibles :**
* Serveur interne : `192.168.0.12`
* Port : `8080`
* Cible : Utilisateur **DELLAA Abderrahmen**

**Votre mission :**
Trouver la vulnérabilité de redirection et l'utiliser comme tremplin pour forcer le Stock Checker à visiter le serveur interne.