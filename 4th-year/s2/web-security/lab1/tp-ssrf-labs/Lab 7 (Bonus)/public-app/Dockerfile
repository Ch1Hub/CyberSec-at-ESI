FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances
RUN pip install flask requests

# Copie du code
COPY . .

# Lancement
CMD ["python", "app.py"]