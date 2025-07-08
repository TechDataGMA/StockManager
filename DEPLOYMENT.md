# Documentation du Déploiement Automatique - StockManager

## Vue d'ensemble

Ce projet utilise un système de déploiement automatique basé sur Docker et GitHub Actions pour déployer l'application StockManager. Le système est inspiré du déploiement d'un autre projet Django mais adapté spécifiquement aux besoins de StockManager.

## Architecture du Déploiement

### 1. Containerisation avec Docker

**Dockerfile**
- Image de base : `python:3.12-slim`
- Timezone configurée pour l'Ukraine (`Europe/Kyiv`)
- Installation de SQLite pour la base de données
- Environnement virtuel Python
- Port d'exposition : 8005 (spécifique à StockManager)
- Script d'entrée pour les migrations et collecte des fichiers statiques

**docker-compose.yml**
- Service principal `stockmanager` sur le port 8005
- Volumes persistants pour la base de données, fichiers statiques et logs
- Service de test optionnel avec profil dédié
- Configuration pour gunicorn en production

### 2. Pipeline CI/CD avec GitHub Actions

**Étapes du pipeline (.github/workflows/deploy.yml) :**

1. **Tests et Validation**
   - Installation de Python 3.12
   - Installation des dépendances
   - Exécution des tests Django (`python manage.py test`)
   - Exécution des tests pytest
   - Vérification de la collecte des fichiers statiques

2. **Build Docker**
   - Configuration du registry Docker insécurisé
   - Setup de Docker Buildx pour multi-architecture
   - Login au registry privé
   - Build et push de l'image pour architecture ARM64
   - Cache des layers Docker pour optimiser les builds

3. **Déploiement**
   - Connexion SSH au serveur de déploiement
   - Exécution du script de déploiement

### 3. Configuration des Paramètres

**Structure des settings Django :**
- `settings/base.py` : Configuration commune
- `settings/development.py` : Configuration de développement
- `settings/production.py` : Configuration de production avec sécurité renforcée
- `settings/__init__.py` : Chargement par défaut du développement

**Spécificités de production :**
- Debug désactivé
- Configuration de sécurité (XSS, Content-Type, X-Frame-Options)
- Logging vers fichier
- Collecte des fichiers statiques dans `staticfiles/`

### 4. Script de Déploiement

**deploy.sh** - Script intelligent qui :
- Vérifie les prérequis (Docker, Docker Compose)
- Gère les réseaux Docker
- Effectue une sauvegarde automatique de la base de données
- Déploie la nouvelle version avec zéro downtime
- Effectue un test de santé de l'application
- Nettoie les ressources inutilisées

## Variables d'Environnement et Secrets

### Secrets GitHub requis :

```
REGISTRY_URL          # URL du registry Docker privé
REGISTRY_USERNAME     # Nom d'utilisateur du registry
REGISTRY_PASSWORD     # Mot de passe du registry
DEPLOY_HOST          # Adresse du serveur de déploiement
DEPLOY_PORT          # Port SSH du serveur
DEPLOY_USER          # Utilisateur SSH
DEPLOY_PATH          # Chemin sur le serveur où déployer
SSH_PRIVATE_KEY      # Clé privée SSH
SSH_PASSPHRASE       # Passphrase de la clé SSH (si applicable)
```

### Variables d'environnement sur le serveur :

```
SECRET_KEY           # Clé secrète Django pour la production
ALLOWED_HOST         # Host autorisé pour Django
```

## Différences avec le Projet d'Origine

### Adaptations spécifiques à StockManager :

1. **Port d'application** : 8005 au lieu de 8003
2. **Base de données** : SQLite au lieu de PostgreSQL
3. **Nom d'image** : `stockmanager` au lieu de `shop-oscar-amartyne`
4. **Timezone** : Europe/Kyiv pour l'Ukraine
5. **Langue** : Configuration ukrainienne (`LANGUAGE_CODE = "uk"`)
6. **Tests** : Intégration de pytest en plus des tests Django
7. **Simplicité** : Pas de dépendances complexes comme les libs d'images HEIF

### Optimisations ajoutées :

1. **Test de santé** : Vérification curl après déploiement
2. **Sauvegarde automatique** : Backup de la DB avant déploiement
3. **Logging amélioré** : Messages colorés dans le script de déploiement
4. **Gestion d'erreurs** : Trap et cleanup en cas d'échec
5. **Cache Docker** : Optimisation des temps de build

## Utilisation

### Déploiement local avec Docker :

```bash
# Build de l'image
docker build -t stockmanager .

# Démarrage avec docker-compose
docker-compose up -d

# Tests
docker-compose --profile test run stockmanager-test
```

### Déploiement automatique :

1. Configurer les secrets GitHub
2. Pousser sur la branche `main`
3. Le pipeline se déclenche automatiquement

### Déploiement manuel sur serveur :

```bash
# Sur le serveur
cd /path/to/stockmanager
./deploy.sh
```

## Surveillance et Maintenance

### Logs de l'application :
```bash
docker logs stockmanager-app
```

### Fichiers de logs persistants :
- `/app/logs/prod.txt` dans le conteneur
- `./logs/prod.txt` sur l'hôte

### Commandes utiles :
```bash
# Redémarrage
docker restart stockmanager-app

# Status
docker ps | grep stockmanager

# Nettoyage
docker system prune -f
```

## Sécurité

- Clé secrète Django configurée via variable d'environnement
- Debug désactivé en production
- Headers de sécurité configurés
- Registry Docker privé avec authentification
- Connexion SSH avec clé privée

Cette architecture de déploiement assure une mise en production automatisée, sécurisée et facilement maintenue pour l'application StockManager.
