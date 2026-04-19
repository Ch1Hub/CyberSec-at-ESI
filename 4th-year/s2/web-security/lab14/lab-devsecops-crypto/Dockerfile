# Utilisation d'une image de base moderne et minimisée (Remédiation du TP 12)
FROM python:3.10-alpine

# Création d'un utilisateur non privilégié (Remédiation du TP 12)
RUN adduser -D myuser

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY app.py .

# Bascule sur l'utilisateur non-root avant l'exécution
USER myuser

EXPOSE 5000

# Lancement de l'application
CMD ["python", "app.py"]