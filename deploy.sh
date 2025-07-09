#!/bin/bash

# Script de déploiement pour StockManager (version docker-compose)
set -e

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

trap 'if [ $? -ne 0 ]; then print_error "Erreur détectée pendant le déploiement"; fi' EXIT

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

# Vérification/copie du .env
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        print_success ".env créé à partir de .env.example"
    else
        print_warning ".env absent et .env.example introuvable !"
    fi
else
    print_success ".env déjà présent"
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

# Pull de la dernière image et déploiement
print_message "Récupération de la dernière image et déploiement..."
docker-compose pull
print_success "Images mises à jour"

docker-compose up -d --remove-orphans
print_success "Services démarrés via docker-compose"

# Vérification que l'application fonctionne
print_message "Vérification que l'application fonctionne..."
sleep 10
if curl -f http://localhost:8005/ &> /dev/null; then
    print_success "Application accessible sur le port 8005"
else
    print_warning "L'application n'est pas encore accessible, vérification des logs..."
    docker-compose logs --tail=20
fi

# Nettoyage des anciennes images
print_message "Nettoyage des anciennes images..."
docker image prune -f
print_success "Images inutilisées supprimées"

print_success "🎉 Déploiement de StockManager terminé avec succès!"
print_message "📊 Informations de déploiement:"
print_message "   - Application: StockManager"
print_message "   - Port: 8005"
print_message "   - Fichier .env: $(pwd)/.env"
print_message "   - Fichier docker-compose.yml: $(pwd)/docker-compose.yml"

print_message "📝 Commandes utiles:"
print_message "   - Voir les logs: docker-compose logs -f"
print_message "   - Redémarrer: docker-compose restart"
print_message "   - Arrêter: docker-compose down"
print_message "   - Statut: docker-compose ps"

print_success "✅ Déploiement terminé!"
