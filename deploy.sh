#!/bin/bash

# Script de déploiement pour StockManager
# Ce script gère la mise à jour de l'application en production

set -e  # Arrêt en cas d'erreur

echo "🚀 Début du déploiement de StockManager..."

# Variables de configuration
REGISTRY_URL=${REGISTRY_URL:-"votre-registry.com"}
IMAGE_NAME="stockmanager"
CONTAINER_NAME="stockmanager-app"
NETWORK_NAME="stockmanager-network"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_message() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Fonction de nettoyage en cas d'erreur
cleanup() {
    if [ $? -ne 0 ]; then
        print_error "Erreur détectée pendant le déploiement"
        print_warning "Nettoyage en cours..."
        # Ici on pourrait ajouter des actions de rollback si nécessaire
    fi
}

trap cleanup EXIT

# Vérification des prérequis
print_message "Vérification des prérequis..."

if ! command -v docker &> /dev/null; then
    print_error "Docker n'est pas installé"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose n'est pas installé"
    exit 1
fi

print_success "Prérequis vérifiés"

# Création du réseau Docker si nécessaire
print_message "Vérification du réseau Docker..."
if ! docker network ls | grep -q "$NETWORK_NAME"; then
    print_message "Création du réseau $NETWORK_NAME..."
    docker network create $NETWORK_NAME
    print_success "Réseau $NETWORK_NAME créé"
else
    print_success "Réseau $NETWORK_NAME existe déjà"
fi

# Connexion au registry et récupération de la dernière image
print_message "Connexion au registry et récupération de l'image..."
docker pull $REGISTRY_URL/$IMAGE_NAME:latest
print_success "Image récupérée depuis le registry"

# Arrêt et suppression du conteneur existant (si il existe)
print_message "Arrêt du conteneur existant..."
if docker ps -a | grep -q "$CONTAINER_NAME"; then
    docker stop $CONTAINER_NAME || true
    docker rm $CONTAINER_NAME || true
    print_success "Ancien conteneur supprimé"
else
    print_warning "Aucun conteneur existant trouvé"
fi

# Sauvegarde de la base de données (si elle existe)
print_message "Sauvegarde de la base de données..."
if [ -f "./db.sqlite3" ]; then
    cp ./db.sqlite3 "./db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)"
    print_success "Base de données sauvegardée"
else
    print_warning "Aucune base de données existante trouvée"
fi

# Création des répertoires nécessaires
print_message "Création des répertoires..."
mkdir -p staticfiles media logs
print_success "Répertoires créés"

# Démarrage du nouveau conteneur
print_message "Démarrage du nouveau conteneur..."
docker run -d \
    --name $CONTAINER_NAME \
    --network $NETWORK_NAME \
    -p 8005:8005 \
    -v $(pwd)/db.sqlite3:/app/db.sqlite3 \
    -v $(pwd)/staticfiles:/app/staticfiles \
    -v $(pwd)/media:/app/media \
    -v $(pwd)/logs:/app/logs \
    -e DJANGO_SETTINGS_MODULE=stockmanager.settings.production \
    -e SECRET_KEY=${SECRET_KEY:-"change-me-in-production"} \
    -e ALLOWED_HOST=${ALLOWED_HOST:-"localhost"} \
    --restart unless-stopped \
    $REGISTRY_URL/$IMAGE_NAME:latest \
    bash -c "source /app/venv/bin/activate && gunicorn stockmanager.wsgi:application --bind 0.0.0.0:8005 --workers 2 --timeout 60 --log-level info"

print_success "Conteneur démarré"

# Vérification que l'application fonctionne
print_message "Vérification que l'application fonctionne..."
sleep 10  # Attendre que l'application démarre

# Test de santé basique
if curl -f http://localhost:8005/ &> /dev/null; then
    print_success "Application accessible sur le port 8005"
else
    print_warning "L'application n'est pas encore accessible, vérification des logs..."
    docker logs $CONTAINER_NAME --tail 20
fi

# Nettoyage des anciennes images
print_message "Nettoyage des anciennes images..."
docker image prune -f
print_success "Images inutilisées supprimées"

# Affichage des informations de fin
print_success "🎉 Déploiement de StockManager terminé avec succès!"
print_message "📊 Informations de déploiement:"
print_message "   - Application: StockManager"
print_message "   - Port: 8005"
print_message "   - Conteneur: $CONTAINER_NAME"
print_message "   - Réseau: $NETWORK_NAME"
print_message "   - Image: $REGISTRY_URL/$IMAGE_NAME:latest"

print_message "📝 Commandes utiles:"
print_message "   - Voir les logs: docker logs $CONTAINER_NAME"
print_message "   - Redémarrer: docker restart $CONTAINER_NAME"
print_message "   - Arrêter: docker stop $CONTAINER_NAME"
print_message "   - Statut: docker ps | grep $CONTAINER_NAME"

echo ""
print_success "✅ Déploiement terminé!"
