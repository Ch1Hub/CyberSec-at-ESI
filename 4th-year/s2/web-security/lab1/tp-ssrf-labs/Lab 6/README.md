# TP SSRF (LAB 6) : Blind SSRF (Detection Out-of-Band)
**ESI SBA - 04 ème année Cys**

## 🎯 Objectif
L'application analyse le header HTTP `Referer` pour des statistiques.
Contrairement aux labs précédents, le résultat de la requête faite par le serveur **n'est pas affiché** sur la page web. C'est une vulnérabilité **Blind SSRF** (Aveugle).

Pour prouver la faille, vous devez forcer le serveur à se connecter à un système externe que vous contrôlez.

## 🛠️ Outils Nécessaires
Puisque **Burp Suite Community** ne possède pas *Burp Collaborator*, nous allons utiliser une alternative gratuite en ligne :
👉 **[Webhook.site](https://webhook.site)**