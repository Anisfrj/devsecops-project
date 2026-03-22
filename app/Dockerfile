# Image de base récente et légère 
FROM python:3.12-alpine

WORKDIR /app

# Copier et installer les dépendances d'abord (cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY app.py .

RUN apk upgrade --no-cache

# ⚠️ Sécurité : ne pas tourner en root
RUN adduser -D appuser
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
