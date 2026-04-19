# DevSecOps & Applied Cryptography Labs

Bienvenue dans l'environnement de travail dédié aux modules de sécurité web avancée et DevSecOps.

Ce dépôt contient une application web volontairement vulnérable. L'objectif principal de ces travaux pratiques est de vous faire transitionner d'un code fonctionnel mais précaire, vers une architecture robuste répondant aux standards modernes de l'industrie.

## 🎯 Objectifs des Ateliers

Cet environnement couvre deux ateliers complémentaires :

- **Workshop No. 14 : DevSecOps & Secret Management (HashiCorp Vault)**
  - **Le problème :** Les secrets (clés d'API, clés cryptographiques) codés en dur dans le code source sont des déchets toxiques.
  - **La mission :** Déployer une infrastructure de gestion de clés (KMS) avec HashiCorp Vault, externaliser la clé de chiffrement maîtresse, et modifier l'application pour qu'elle récupère ce secret dynamiquement en mémoire via une authentification robuste (AppRole).
- **Workshop No. 15 : Cryptography Refactoring ("Roll Your Own Crypto")**
  - **Le problème :** L'application utilise des algorithmes obsolètes (MD5 sans sel) et des implémentations dangereuses (AES en mode ECB avec du padding manuel).
  - **La mission :** Supprimer cette "plomberie" cryptographique maison. Vous devrez implémenter les standards actuels : le hachage de mots de passe avec **Argon2id** et le chiffrement authentifié (AEAD) avec **AES-GCM**, en utilisant la clé sécurisée par Vault.

---

## 🛠️ Prérequis

Pour réaliser ces TPs, vous aurez besoin des outils suivants installés et configurés sur votre machine :

- **Python 3.8+** (avec `pip` installé)
- **Docker** et **Docker Compose**
- **Git**
- **curl** (ou un outil comme Postman/Insomnia pour tester l'API)

---

## 🚀 Mise en place de l'environnement (Setup)

Afin de faciliter la modification du code Python en temps réel sans avoir à recompiler des conteneurs à chaque ligne, nous allons adopter une **approche hybride** : l'infrastructure de sécurité (Vault) tournera sous Docker, tandis que l'application Flask sera exécutée localement.

### Étape 1 : Préparation de l'application locale

1. Ouvrez un terminal à la racine de ce projet.
2. _(Optionnel mais recommandé)_ Créez et activez un environnement virtuel Python pour isoler vos dépendances :
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```
3. Installez les dépendances requises pour l'application :
   ```bash
   pip install -r requirements.txt
   ```

### Étape 2 : Lancement de l'infrastructure (HashiCorp Vault)

Nous utilisons Docker Compose pour lancer Vault en mode développement.

1. Démarrez le service Vault en tâche de fond :
   ```bash
   docker run -d --name=dev-vault -p 8200:8200 --entrypoint vault hashicorp/vault server -dev -dev-listen-address="0.0.0.0:8200" -dev-root-token-id="root"
   ```
2. Vérifiez que le conteneur tourne correctement et que l'API de Vault répond sur le port 8200 :
   ```bash
   curl [http://127.0.0.1:8200/v1/sys/health](http://127.0.0.1:8200/v1/sys/health)
   ```
   _(Vous devriez recevoir une réponse JSON confirmant l'état du serveur)._

### Étape 3 : Configuration de l'authentification AppRole et des Politiques

En DevSecOps, une application ne doit jamais utiliser un token "root". Elle doit s'authentifier en tant que machine avec un rôle spécifique et des droits limités (Principe de moindre privilège). Nous allons configurer l'authentification **AppRole**.

Pour simplifier la saisie des commandes, nous allons ouvrir un terminal interactif directement à l'intérieur du conteneur Vault :

1. Entrez dans le conteneur avec les variables d'environnement appropriées :
   ```bash
   docker exec -e VAULT_ADDR='[http://127.0.0.1:8200](http://127.0.0.1:8200)' -e VAULT_TOKEN='root' -it dev-vault /bin/sh
   ```
   *(Votre invite de commande se transforme en `/ #`. Vous êtes à l'intérieur du conteneur Vault !)*

2. Activez le moteur d'authentification AppRole :
   ```bash
   vault auth enable approle
   ```

3. Créez une politique stricte (`webapp-policy`) qui autorise uniquement la lecture de notre secret. Copiez-collez ce bloc entier :
   ```bash
   vault policy write webapp-policy - <<EOF
   path "secret/data/myapp" {
     capabilities = ["read"]
   }
   EOF
   ```

4. Créez le rôle applicatif (`webapp`) et attachez-lui la politique :
   ```bash
   vault write auth/approle/role/webapp policies="webapp-policy" token_ttl=1h token_max_ttl=4h
   ```

5. Générez et récupérez les identifiants de l'application (l'équivalent d'un login/mot de passe pour les machines) :
   
   **Récupérez le Role ID :**
   ```bash
   vault read auth/approle/role/webapp/role-id
   ```
   
   **Générez un Secret ID :**
   ```bash
   vault write -f auth/approle/role/webapp/secret-id
   ```

6. Notez précieusement le `role_id` et le `secret_id` générés, puis quittez le conteneur :
   ```bash
   exit
   ```

---

### Étape 4 : Mise à jour de l'application Python

Maintenant que Vault est configuré pour accepter votre application, vous devez injecter ces identifiants dans votre code.

1. Ouvrez le fichier `app.py` (ou votre fichier `.env` si vous l'utilisez).
2. Remplacez les valeurs des variables `ROLE_ID` et `SECRET_ID` par celles que vous venez de générer à l'étape précédente.
3. Lancez votre serveur Flask :
   ```bash
   python app.py
   ```
   *(Le serveur devrait démarrer avec succès et afficher `* Running on http://127.0.0.1:5000`)*
---

## 💡 Conseils pour le déroulement des TPs

- **Gestion des terminaux :** Gardez toujours au moins deux terminaux ouverts. Utilisez le premier pour faire tourner le serveur Flask (`app.py`), et utilisez le second pour interagir avec Vault via la CLI Docker ou pour envoyer vos requêtes `curl` à l'API.
- **Redémarrage :** À chaque fois que vous modifiez le fichier `app.py` lors des phases de remédiation, n'oubliez pas d'arrêter le serveur Flask (`CTRL+C`) et de le relancer pour que vos modifications soient prises en compte.
