# TP4/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copier uniquement les fichiers nécessaires
COPY TP4.2.py .
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Point d'entrée
CMD ["python", "TP4.2.py"]