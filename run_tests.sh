#!/bin/bash

# Script pour lancer les tests de l'application Stock Manager
# Usage: ./run_tests.sh [options]

set -e

echo "🧪 Lancement des tests pour Stock Manager"
echo "========================================"

# Couleurs pour l'affichage
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction d'aide
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Afficher cette aide"
    echo "  -v, --verbose       Mode verbeux"
    echo "  -c, --coverage      Lancer avec couverture de code"
    echo "  -r, --report        Générer rapport HTML de couverture"
    echo "  -f, --failfast      Arrêter au premier échec"
    echo "  -k, --keepdb        Garder la base de test (plus rapide)"
    echo ""
    echo "Exemples:"
    echo "  $0                  # Tests simples"
    echo "  $0 -c               # Tests avec couverture"
    echo "  $0 -c -r            # Tests avec rapport HTML"
    echo "  $0 -v -f            # Tests verbeux qui s'arrêtent au premier échec"
}

# Paramètres par défaut
VERBOSE=""
COVERAGE=""
REPORT=""
FAILFAST=""
KEEPDB=""

# Parse des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--verbose)
            VERBOSE="-v 2"
            shift
            ;;
        -c|--coverage)
            COVERAGE=1
            shift
            ;;
        -r|--report)
            REPORT=1
            shift
            ;;
        -f|--failfast)
            FAILFAST="--failfast"
            shift
            ;;
        -k|--keepdb)
            KEEPDB="--keepdb"
            shift
            ;;
        *)
            echo "Option inconnue: $1"
            show_help
            exit 1
            ;;
    esac
done

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "manage.py" ]; then
    echo -e "${RED}❌ Erreur: manage.py non trouvé. Exécutez ce script depuis le répertoire racine du projet.${NC}"
    exit 1
fi

# Lancer les tests
if [ "$COVERAGE" = "1" ]; then
    echo -e "${BLUE}📊 Lancement des tests avec couverture de code...${NC}"
    coverage run --source='.' manage.py test inventory.tests $VERBOSE $FAILFAST $KEEPDB
    
    echo -e "${BLUE}📈 Génération du rapport de couverture...${NC}"
    coverage report --include="inventory/*"
    
    if [ "$REPORT" = "1" ]; then
        echo -e "${BLUE}🌐 Génération du rapport HTML...${NC}"
        coverage html --include="inventory/*"
        echo -e "${GREEN}✅ Rapport HTML généré dans htmlcov/index.html${NC}"
    fi
else
    echo -e "${BLUE}🏃 Lancement des tests...${NC}"
    python manage.py test inventory.tests $VERBOSE $FAILFAST $KEEPDB
fi

echo ""
echo -e "${GREEN}✅ Tests terminés avec succès !${NC}"

# Statistiques finales
if [ "$COVERAGE" = "1" ]; then
    echo ""
    echo -e "${BLUE}📋 Résumé de la couverture:${NC}"
    coverage report --include="inventory/*" | tail -1
fi
