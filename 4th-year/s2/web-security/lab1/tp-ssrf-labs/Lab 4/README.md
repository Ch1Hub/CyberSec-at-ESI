# TP SSRF (LAB 4) : Bypass Whitelist (Niveau Expert)
**ESI SBA - 04ème année Cys**

## 🎯 Objectif
Dans ce scénario, le développeur a mis en place une défense robuste : une **Whitelist**.
L'application refuse catégoriquement toute URL qui ne semble pas appartenir au domaine légitime : `stock.shop-internal.net`.

**Votre mission :**
Utiliser des techniques avancées d'obfuscation d'URL (Embedded Credentials & URL Fragment) pour tromper le validateur et forcer le serveur à se connecter à `localhost` pour supprimer l'utilisateur **DELLAA Abderrahmen**.