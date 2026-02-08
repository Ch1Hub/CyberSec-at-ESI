# TP SSRF (LAB 3) : Contournement de Filtres (Blacklist)

**ESI SBA - 04ème année Cys**

## 🎯 Objectif

Dans ce scénario, une vulnérabilité SSRF existe, mais le développeur a implémenté des protections de type "Blacklist" (Liste noire).

**Les protections en place :**

1.  **Filtre d'Hôte :** Bloque strictement `127.0.0.1` et `localhost`.
2.  **Filtre d'URL :** Bloque toute URL contenant le mot `admin`.

**Votre mission :**
Trouver comment contourner ces deux vérifications pour accéder à `http://localhost/admin` et supprimer l'utilisateur **Djamel Bensaber**.