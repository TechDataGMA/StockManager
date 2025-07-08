#!/bin/bash

# Script de test local pour StockManager
# Vérifie que l'application fonctionne correctement

set -e

echo "🧪 Tests locaux pour StockManager"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Test 1: Vérification des dépendances
print_info "Vérification des dépendances Python..."
python -c "
import django
import PIL
import pytest
print(f'Django version: {django.get_version()}')
print('Toutes les dépendances sont installées')
"
print_success "Dépendances OK"

# Test 2: Tests Django
print_info "Exécution des tests Django..."
python manage.py test --verbosity=0
print_success "Tests Django passés"

# Test 3: Tests pytest (optionnel)
print_info "Exécution des tests pytest..."
if pytest --collect-only &> /dev/null; then
    pytest -v
    print_success "Tests pytest passés"
else
    print_info "Aucun test pytest trouvé, test ignoré"
fi

# Test 4: Vérification des migrations
print_info "Vérification des migrations..."
python manage.py makemigrations --check --dry-run
print_success "Migrations à jour"

# Test 5: Collecte des fichiers statiques
print_info "Test de collecte des fichiers statiques..."
python manage.py collectstatic --noinput --settings=stockmanager.settings.production > /dev/null 2>&1
print_success "Fichiers statiques collectés"

# Test 6: Vérification de la configuration
print_info "Vérification de la configuration..."
python manage.py check --settings=stockmanager.settings.production
print_success "Configuration valide"

# Test 7: Test Docker build (si Docker est disponible)
if command -v docker &> /dev/null; then
    print_info "Test de build Docker..."
    docker build -t stockmanager-test . > /dev/null 2>&1
    print_success "Image Docker buildée avec succès"
    
    # Nettoyage
    docker rmi stockmanager-test > /dev/null 2>&1
else
    print_info "Docker non disponible, test de build ignoré"
fi

# Test 8: Vérification des traductions ukrainiennes
print_info "Vérification des traductions ukrainiennes..."
python -c "
from django.conf import settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockmanager.settings')
import django
django.setup()

# Vérifier que la langue est bien configurée en ukrainien
assert settings.LANGUAGE_CODE == 'uk', f'Langue attendue: uk, trouvée: {settings.LANGUAGE_CODE}'
assert settings.TIME_ZONE == 'Europe/Kyiv', f'Timezone attendue: Europe/Kyiv, trouvée: {settings.TIME_ZONE}'
print('Configuration ukrainienne OK')
"
print_success "Configuration ukrainienne valide"

echo ""
print_success "🎉 Tous les tests locaux sont passés!"
print_info "L'application est prête pour le déploiement"
