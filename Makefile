# Makefile pour StockManager
# Simplifie les commandes courantes de développement et déploiement

.PHONY: help install test run docker-build docker-run docker-test deploy-local clean

# Variables
PYTHON = python
PIP = pip
DOCKER = docker
COMPOSE = docker-compose

help: ## Affiche cette aide
	@echo "Commandes disponibles pour StockManager :"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Installe les dépendances Python
	$(PIP) install -r requirements.txt

test: ## Lance tous les tests
	$(PYTHON) manage.py test
	@echo "✅ Tests Django terminés"
	./test_local.sh

test-django: ## Lance uniquement les tests Django
	$(PYTHON) manage.py test --verbosity=2

test-coverage: ## Lance les tests avec couverture de code
	coverage run --source='.' manage.py test
	coverage report -m
	coverage html

run: ## Lance le serveur de développement
	$(PYTHON) manage.py runserver

run-prod: ## Lance le serveur en mode production
	$(PYTHON) manage.py collectstatic --noinput --settings=stockmanager.settings.production
	$(PYTHON) manage.py migrate --settings=stockmanager.settings.production
	gunicorn stockmanager.wsgi:application --bind 127.0.0.1:8005 --settings=stockmanager.settings.production

migrate: ## Applique les migrations
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

collectstatic: ## Collecte les fichiers statiques
	$(PYTHON) manage.py collectstatic --noinput

superuser: ## Crée un superutilisateur
	$(PYTHON) manage.py createsuperuser

docker-build: ## Build l'image Docker
	$(DOCKER) build -t stockmanager .

docker-run: ## Lance l'application avec Docker
	$(COMPOSE) up -d

docker-test: ## Lance les tests dans Docker
	$(COMPOSE) --profile test run stockmanager-test

docker-logs: ## Affiche les logs Docker
	$(COMPOSE) logs -f stockmanager

docker-stop: ## Arrête les conteneurs Docker
	$(COMPOSE) down

docker-clean: ## Nettoie les images Docker inutilisées
	$(DOCKER) system prune -f
	$(DOCKER) image prune -f

deploy-local: ## Déploie localement avec le script
	./deploy.sh

populate-data: ## Peuple la base avec des données de test
	$(PYTHON) populate_test_data.py

clean: ## Nettoie les fichiers temporaires
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf staticfiles/

format: ## Formate le code avec black (si installé)
	@if command -v black >/dev/null 2>&1; then \
		black .; \
	else \
		echo "Black n'est pas installé. Installer avec: pip install black"; \
	fi

lint: ## Vérifie le code avec flake8 (si installé)
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 .; \
	else \
		echo "Flake8 n'est pas installé. Installer avec: pip install flake8"; \
	fi

check: ## Vérification complète (tests + qualité code)
	$(PYTHON) manage.py check
	make test
	@echo "✅ Vérification complète terminée"

backup-db: ## Sauvegarde la base de données
	@if [ -f "db.sqlite3" ]; then \
		cp db.sqlite3 "db.sqlite3.backup.$$(date +%Y%m%d_%H%M%S)"; \
		echo "✅ Base de données sauvegardée"; \
	else \
		echo "❌ Aucune base de données trouvée"; \
	fi

init: ## Initialisation complète du projet
	make install
	make migrate
	make collectstatic
	@echo "✅ Projet initialisé"
	@echo "Pour créer un superutilisateur : make superuser"
	@echo "Pour lancer le serveur : make run"
