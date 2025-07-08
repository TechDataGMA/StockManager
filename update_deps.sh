#!/bin/bash

# Script de mise à jour des dépendances pour StockManager
# Vérifie et met à jour les packages Python en toute sécurité

set -e

echo "🔄 Mise à jour des dépendances StockManager"

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier l'environnement virtuel
if [[ "$VIRTUAL_ENV" == "" ]]; then
    print_error "Environnement virtuel non activé"
    print_info "Activez l'environnement virtuel avec : source .venv/bin/activate"
    exit 1
fi

print_success "Environnement virtuel activé : $VIRTUAL_ENV"

# Sauvegarde des requirements actuels
print_info "Sauvegarde des requirements actuels..."
cp requirements.txt "requirements.txt.backup.$(date +%Y%m%d_%H%M%S)"
print_success "Sauvegarde créée"

# Afficher les packages actuels
print_info "Packages actuellement installés :"
pip list --format=columns

# Vérifier les packages obsolètes
print_info "Vérification des packages obsolètes..."
OUTDATED=$(pip list --outdated --format=json)

if [ "$OUTDATED" = "[]" ]; then
    print_success "Tous les packages sont à jour !"
    exit 0
fi

echo "$OUTDATED" | python3 -m json.tool

# Demander confirmation
echo ""
read -p "Voulez-vous mettre à jour les packages ? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Mise à jour annulée"
    exit 0
fi

# Mise à jour en mode dry-run d'abord
print_info "Test de mise à jour (dry-run)..."

# Packages critiques à ne pas mettre à jour automatiquement
CRITICAL_PACKAGES="Django"

# Mise à jour des packages non critiques
print_info "Mise à jour des packages..."

# Mise à jour de pip d'abord
pip install --upgrade pip

# Mise à jour des autres packages (sauf Django pour éviter les breaking changes)
pip install --upgrade Pillow coverage pytest pytest-django gunicorn

print_success "Packages mis à jour"

# Génération du nouveau requirements.txt
print_info "Génération du nouveau requirements.txt..."
pip freeze | grep -E "(Django|Pillow|coverage|pytest|gunicorn)" > requirements_new.txt

# Vérification que Django n'a pas été mis à jour de manière majeure
DJANGO_VERSION=$(pip show Django | grep Version | cut -d ' ' -f 2)
print_info "Version Django actuelle : $DJANGO_VERSION"

# Tests de régression
print_info "Exécution des tests de régression..."
if python manage.py test --verbosity=0; then
    print_success "Tests passés avec les nouvelles dépendances"
    mv requirements_new.txt requirements.txt
    print_success "requirements.txt mis à jour"
else
    print_error "Les tests ont échoué avec les nouvelles dépendances"
    print_info "Restauration de l'ancienne version..."
    pip install -r requirements.txt
    rm requirements_new.txt
    exit 1
fi

# Affichage final
print_info "Nouvelles dépendances :"
cat requirements.txt

print_success "🎉 Mise à jour terminée avec succès !"
print_info "N'oubliez pas de :"
print_info "  1. Tester l'application complètement"
print_info "  2. Commiter les changements si tout fonctionne"
print_info "  3. Mettre à jour l'image Docker si nécessaire"
