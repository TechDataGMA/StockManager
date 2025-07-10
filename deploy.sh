#!/bin/bash

# Charger les variables d'environnement depuis .env s'il existe
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

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

# Sauvegarde de la base de données SQLite avant déploiement
if [ -f db.sqlite3 ]; then
    BACKUP_NAME="db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)"
    cp db.sqlite3 "$BACKUP_NAME"
    print_success "Sauvegarde de db.sqlite3 -> $BACKUP_NAME"
else
    print_warning "Aucune base de données existante trouvée à sauvegarder."
fi

# Vérification/création du fichier db.sqlite3 (doit être un fichier, pas un dossier)
if [ -d db.sqlite3 ]; then
    print_warning "Suppression du dossier db.sqlite3 qui ne devrait pas exister..."
    rm -rf db.sqlite3
fi
if [ ! -f db.sqlite3 ]; then
    print_message "Création du fichier db.sqlite3 vide..."
    touch db.sqlite3
    chmod 664 db.sqlite3
    chown $(id -u):$(id -g) db.sqlite3
    print_success "Fichier db.sqlite3 créé avec succès"
else
    print_success "Fichier db.sqlite3 déjà présent"
fi

# Sauvegarde de la base de données (si elle existe)
print_message "Sauvegarde de la base de données..."
if [ -f "./db.sqlite3" ]; then
    cp ./db.sqlite3 "./db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)"
    print_success "Base de données sauvegardée"
else
    print_warning "Aucune base de données existante trouvée"
fi

# Suppression des backups de plus de 7 jours
find . -maxdepth 1 -name "db.sqlite3.backup.*" -type f -mtime +7 -exec rm -f {} \;
print_success "Backups de plus de 7 jours supprimés"

# Création des répertoires nécessaires
print_message "Création des répertoires..."
mkdir -p staticfiles media logs
print_success "Répertoires créés"

# Connexion au registry Docker privé
print_message "Connexion au registry Docker privé..."
docker login "$REGISTRY_URL" -u "$REGISTRY_USERNAME" -p "$REGISTRY_PASSWORD"
if [ $? -ne 0 ]; then
    print_error "Échec de l'authentification au registry Docker privé"
    exit 1
fi
print_success "Authentification au registry réussie"

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
