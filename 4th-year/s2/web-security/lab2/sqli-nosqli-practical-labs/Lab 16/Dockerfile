FROM python:3.9-slim

WORKDIR /app

# 1. On copie d'abord SEULEMENT le fichier requirements
COPY requirements.txt .

# 2. Maintenant qu'il est là, on peut l'installer
RUN pip install --no-cache-dir -r requirements.txt

# 3. Ensuite, on copie tout le reste du code (app.py, templates, etc.)
COPY . .

CMD ["python", "app.py"]