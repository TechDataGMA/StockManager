FROM python:3.12-slim

ARG DJANGO_ENV=production

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    git \
    gcc \
    libc6-dev \
    sqlite3 \
    curl \
    tzdata \
    && ln -sf /usr/share/zoneinfo/Europe/Kyiv /etc/localtime \
    && echo "Europe/Kyiv" > /etc/timezone \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copie du code source
COPY . .

# Configuration de l'environnement virtuel
RUN python -m venv /app/venv

# Activer l'environnement virtuel et installer les dépendances
RUN /bin/bash -c "source /app/venv/bin/activate \
    && pip install --upgrade pip setuptools \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn"

# Installer uv (gestionnaire de paquets rapide)
RUN /app/venv/bin/pip install uv

# Installer les dépendances Python avec uv
RUN /bin/bash -c "source /app/venv/bin/activate \
    && uv pip install --upgrade pip setuptools \
    && uv pip install --no-cache-dir -r requirements.txt \
    && uv pip install gunicorn"

# Création des répertoires nécessaires
RUN mkdir -p /app/staticfiles /app/media /app/logs \
    && touch /app/logs/prod.txt

# Variables d'environnement pour Django
ENV DJANGO_SETTINGS_MODULE=stockmanager.settings.production
ENV PYTHONPATH=/app

# Script d'entrée pour collecter les fichiers statiques et faire les migrations
RUN echo '#!/bin/bash\n\
source /app/venv/bin/activate\n\
python manage.py collectstatic --noinput\n\
python manage.py migrate --noinput\n\
exec "$@"' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Exposer le port 8005 pour StockManager
EXPOSE 8005

ENTRYPOINT ["/app/entrypoint.sh"]
