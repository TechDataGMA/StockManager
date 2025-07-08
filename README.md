# Gestion des Entrées/Sorties de Marchandises

Application Django complète pour la gestion des stocks avec interface en ukrainien.

## Fonctionnalités

### 🏪 Gestion des Produits
- ✅ Création, modification, suppression des produits
- ✅ Description, coût d'achat, prix de vente de base
- ✅ Seuil d'alerte personnalisable
- ✅ Calcul automatique du stock actuel
- ✅ Valeur du stock en cours
- ✅ **Prix négociés multiples** par produit
- ✅ **Historique des prix** avec clients et contexte
- ✅ **Activation/désactivation** des prix de vente
- ✅ **Marge bénéficiaire** automatique

### 📊 Tableau de Bord
- ✅ Vue d'ensemble des stocks
- ✅ Statistiques générales
- ✅ Alertes de stock faible/épuisé
- ✅ Historique des derniers mouvements
- ✅ Indicateurs visuels colorés

### 📈 Gestion des Mouvements
- ✅ Enregistrement des entrées/sorties
- ✅ **Prix spécifique** pour chaque sortie
- ✅ **Sélection du prix négocié** lors des sorties
- ✅ Historique complet avec filtres
- ✅ Filtrage par date, type, produit
- ✅ Export CSV des données
- ✅ Commentaires sur les opérations
- ✅ **Valeur des mouvements** calculée automatiquement

### 🎨 Interface Utilisateur
- ✅ Design moderne avec Bootstrap 5
- ✅ Interface entièrement en ukrainien
- ✅ Navigation intuitive avec icônes
- ✅ Design responsive (mobile-friendly)
- ✅ Messages de feedback utilisateur

### ⚠️ Système d'Alertes
- ✅ Alertes produits en rupture
- ✅ Alertes seuil de stock bas
- ✅ Statuts visuels (normal/alerte/rupture)
- ✅ Notifications sur tableau de bord

### 🚀 Déploiement Automatique
- ✅ **Pipeline CI/CD** avec GitHub Actions
- ✅ **Containerisation Docker** complète
- ✅ **Script de déploiement** automatisé
- ✅ **Tests automatiques** avant déploiement
- ✅ **Registry Docker privé** supporté
- ✅ **Zéro downtime** deployment
- ✅ **Monitoring et logs** intégrés

### � Gestion des Prix
- ✅ **Prix de base** pour chaque produit
- ✅ **Prix négociés multiples** par produit
- ✅ **Historique complet** des prix avec dates
- ✅ **Contexte client** pour chaque prix
- ✅ **Commentaires** sur les négociations
- ✅ **Prix actif/inactif** avec basculement
- ✅ **Sélection du prix** lors des sorties
- ✅ **Calcul automatique** des marges

### �📁 Export et Rapports
- ✅ Export CSV des mouvements
- ✅ Filtres avancés
- ✅ Historique détaillé

## Installation

### Installation Rapide avec Makefile

```bash
# Installation complète en une commande
make init

# Créer un superutilisateur
make superuser

# Lancer le serveur
make run
```

### Installation Manuelle

1. Créer un environnement virtuel :
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\activate  # Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
# ou
make install
```

3. Effectuer les migrations :
```bash
python manage.py makemigrations
python manage.py migrate
# ou
make migrate
```

4. Créer un superutilisateur (optionnel) :
```bash
python manage.py createsuperuser
```

5. Lancer le serveur de développement :
```bash
python manage.py runserver
```

L'application sera accessible à l'adresse http://127.0.0.1:8000/

## 🐳 Déploiement avec Docker

### Déploiement Local

1. **Avec Docker Compose** :
```bash
docker-compose up -d
```

2. **Build manuel** :
```bash
docker build -t stockmanager .
docker run -p 8004:8004 stockmanager
```

L'application sera accessible sur http://localhost:8004

### Déploiement en Production

Le projet inclut un système de déploiement automatique complet :

#### Configuration GitHub Actions

1. **Secrets à configurer dans GitHub** :
   - `REGISTRY_URL` : URL du registry Docker privé
   - `REGISTRY_USERNAME` : Nom d'utilisateur registry
   - `REGISTRY_PASSWORD` : Mot de passe registry
   - `DEPLOY_HOST` : Serveur de déploiement
   - `DEPLOY_PORT` : Port SSH
   - `DEPLOY_USER` : Utilisateur SSH
   - `DEPLOY_PATH` : Chemin de déploiement
   - `SSH_PRIVATE_KEY` : Clé privée SSH
   - `SSH_PASSPHRASE` : Passphrase SSH (optionnel)

2. **Variables d'environnement sur le serveur** :
   - `SECRET_KEY` : Clé secrète Django
   - `ALLOWED_HOST` : Host autorisé

#### Pipeline de Déploiement

Le pipeline GitHub Actions :
1. ✅ Exécute tous les tests automatiquement
2. ✅ Build l'image Docker optimisée
3. ✅ Push vers le registry privé
4. ✅ Déploie automatiquement sur le serveur
5. ✅ Effectue les vérifications de santé

#### Déploiement Manuel

Sur le serveur de production :
```bash
cd /path/to/stockmanager
./deploy.sh
```

Le script effectue :
- Sauvegarde automatique de la DB
- Déploiement zero-downtime
- Vérifications de santé
- Nettoyage des ressources

### 🛠️ Commandes Utiles

```bash
# Tests
make test                # Tests complets
make test-django         # Tests Django uniquement
make test-coverage       # Tests avec couverture

# Développement
make run                 # Serveur de développement
make run-prod           # Serveur en mode production
make migrate            # Migrations
make collectstatic      # Fichiers statiques
make superuser          # Créer admin

# Docker
make docker-build       # Build image
make docker-run         # Lancer avec Docker
make docker-test        # Tests dans Docker
make docker-logs        # Voir les logs

# Maintenance
make clean              # Nettoyer fichiers temporaires
make backup-db          # Sauvegarder la DB
make deploy-local       # Déploiement local
make check              # Vérification complète

# Aide
make help               # Liste toutes les commandes
```

## Structure du Projet

```
StockManager/
├── inventory/              # Application principale
│   ├── models.py          # Modèles Produit et Mouvement
│   ├── views.py           # Vues et logique métier
│   ├── forms.py           # Formulaires Django
│   ├── admin.py           # Interface d'administration
│   └── urls.py            # URLs de l'application
├── stockmanager/          # Configuration Django
│   ├── settings.py        # Paramètres (langue ukrainienne)
│   └── urls.py            # URLs principales
├── templates/             # Templates HTML
│   ├── base.html          # Template de base
│   └── inventory/         # Templates de l'app
└── static/                # Fichiers statiques (Bootstrap CDN)
```

## Guide d'Utilisation

### 🚀 Premiers Pas

1. **Accès à l'application** : Ouvrir http://127.0.0.1:8000/
2. **Tableau de bord** : Vue d'ensemble avec alertes et statistiques
3. **Navigation** : Menu principal avec sections Produits, Mouvements, Prix

### 📦 Gestion des Produits

#### Créer un Produit
1. Aller dans "Продукти" → "Додати продукт"
2. Remplir les informations de base :
   - Nom (requis)
   - Description
   - Coût d'achat en euro
   - Prix de vente de base en euro
   - Seuil d'alerte (quantité minimale)
3. Sauvegarder

#### Ajouter des Prix Négociés
1. Depuis la liste des produits → "Деталі" sur un produit
2. Section "Продажні ціни" → "Додати ціну"
3. Saisir :
   - Prix négocié en euro
   - Nom du client (optionnel)
   - Commentaire sur les conditions
4. Le prix devient automatiquement actif

### 📈 Enregistrer des Mouvements

#### Entrée de Stock
1. "Рухи" → "Додати рух"
2. Sélectionner :
   - Type : "Вхід" (Entrée)
   - Produit
   - Quantité
   - Commentaire (optionnel)
3. Le coût total = Quantité × Coût d'achat du produit

#### Sortie de Stock avec Prix Négocié
1. "Рухи" → "Додати рух"
2. Sélectionner :
   - Type : "Вихід" (Sortie)
   - Produit → **Les prix disponibles se chargent automatiquement**
3. Choisir le prix dans la liste déroulante :
   - Prix de base du produit
   - Tous les prix négociés actifs
4. Saisir la quantité
5. La valeur est calculée automatiquement : Quantité × Prix sélectionné

### 🔍 Filtres et Recherche

#### Filtrer les Mouvements
- **Par période** : Date de début et fin
- **Par type** : Entrées, sorties ou tous
- **Par produit** : Sélection dans la liste déroulante
- **Combinaisons** : Tous les filtres sont combinables

#### Export CSV
1. Appliquer les filtres souhaités
2. Cliquer sur "Експорт у CSV"
3. Le fichier contient tous les détails des mouvements filtrés

### ⚠️ Gestion des Alertes

#### Types d'Alertes
- **Stock épuisé** (rouge) : Quantité = 0
- **Stock faible** (orange) : Quantité ≤ seuil d'alerte
- **Stock normal** (vert) : Quantité > seuil d'alerte

#### Surveillance
- Alertes visibles sur le tableau de bord
- Statuts colorés dans la liste des produits
- Compteurs d'alertes en temps réel

## Technologies Utilisées

- **Backend**: Django 5.2.4
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Base de données**: SQLite (par défaut)
- **Langue**: Interface en ukrainien (uk)
- **Monnaie**: Euro (€)
- **CSS Framework**: Bootstrap 5.3.0
- **JavaScript**: AJAX pour interactions dynamiques
- **Timezone**: Europe/Kyiv

## Architecture du Projet

### Modèles de Données

#### Produit (Product)
```python
- nom: CharField (Nom du produit)
- description: TextField (Description détaillée)
- cout_achat: DecimalField (Coût d'achat en euro)
- prix_vente_base: DecimalField (Prix de vente de base en euro)
- seuil_alerte: PositiveIntegerField (Seuil d'alerte stock)
- date_creation: DateTimeField (Date de création automatique)
```

#### Mouvement (Mouvement)
```python
- produit: ForeignKey vers Produit
- type_mouvement: CharField (ENTREE/SORTIE)
- quantite: PositiveIntegerField
- prix_vente_utilise: ForeignKey vers PrixVente (optionnel)
- commentaire: TextField (optionnel)
- date_mouvement: DateTimeField (automatique)
```

#### PrixVente (Prix de Vente)
```python
- produit: ForeignKey vers Produit
- prix: DecimalField (Prix négocié en euro)
- client: CharField (Nom du client, optionnel)
- commentaire: TextField (Conditions de négociation)
- actif: BooleanField (Prix actif/inactif)
- date_creation: DateTimeField (automatique)
```

### Fonctionnalités Techniques

#### Calculs en Temps Réel
- **Stock actuel** : Somme des entrées - Somme des sorties
- **Valeur stock** : Stock × Coût d'achat
- **Marge** : (Prix de vente - Coût d'achat) / Coût d'achat × 100

#### AJAX et Interface Dynamique
- Chargement automatique des prix lors de la sélection d'un produit
- Mise à jour en temps réel des formulaires
- Messages de feedback utilisateur

#### Internationalisation
- Configuration complète en ukrainien
- Formats de date/heure pour l'Ukraine
- Timezone Europe/Kyiv
- Messages d'interface traduits

## Développement et Maintenance

### Structure des Templates
```
templates/
├── base.html                    # Template de base avec Bootstrap
└── inventory/
    ├── tableau_bord.html       # Tableau de bord principal
    ├── liste_produits.html     # Liste des produits avec alertes
    ├── detail_produit.html     # Détail produit + prix négociés
    ├── form_produit.html       # Formulaire produit
    ├── liste_mouvements.html   # Historique des mouvements
    ├── form_mouvement.html     # Formulaire mouvement avec AJAX
    └── form_prix_vente.html    # Formulaire prix négocié
```

### URLs et Navigation
- `/` : Tableau de bord principal
- `/products/` : Gestion des produits
- `/movements/` : Gestion des mouvements
- `/ajax/get-prices/<product_id>/` : API AJAX pour les prix
- `/export-csv/` : Export des données

## Exemple d'Utilisation Complète

### Scénario : Gestion d'un Produit avec Prix Négociés

1. **Création du produit** :
   - Nom : "Ordinateur portable"
   - Coût d'achat : 800€
   - Prix de vente de base : 1200€
   - Seuil d'alerte : 5 unités

2. **Ajout de prix négociés** :
   - Client A (Entreprise) : 1100€ (remise volume)
   - Client B (Particulier fidèle) : 1150€ (fidélité)

3. **Entrée en stock** :
   - Type : Entrée
   - Quantité : 20 unités
   - Valeur d'achat : 20 × 800€ = 16 000€

4. **Vente avec prix négocié** :
   - Type : Sortie
   - Quantité : 3 unités
   - Prix sélectionné : 1100€ (Client A)
   - Valeur de vente : 3 × 1100€ = 3 300€
   - Stock restant : 17 unités

5. **Suivi en temps réel** :
   - Stock actuel : 17 unités (calculé automatiquement)
   - Valeur stock : 17 × 800€ = 13 600€
   - Alerte : Stock normal (> 5 unités)

## Points Forts de l'Application

### 🎯 Flexibilité des Prix
- **Multiple prix par produit** : Adaptation aux différents clients
- **Prix contextualisés** : Association client/contexte pour chaque prix
- **Sélection libre** : Choix du prix à chaque sortie
- **Historique complet** : Traçabilité de tous les prix négociés

### 💶 Gestion Monétaire Rigoureuse
- **Unité unique** : Euro pour tous les montants
- **Précision décimale** : Gestion des centimes
- **Calculs automatiques** : Valeurs et marges en temps réel
- **Export cohérent** : CSV avec montants en euro

### 🚀 Interface Moderne
- **Design responsive** : Adaptation mobile/desktop
- **Interface ukrainienne** : Traduction complète
- **Navigation intuitive** : Structure logique et icônes
- **Feedback utilisateur** : Messages et alertes visuelles

### 📊 Gestion Intelligente
- **Alertes automatiques** : Stock faible/épuisé
- **Calculs en temps réel** : Stock, valeurs, marges
- **Filtres avancés** : Recherche multicritères
- **Export données** : CSV pour analyse externe

## Support et Développement

Cette application Django est configurée pour la production avec :
- **Sécurité** : Protection CSRF, validation des données
- **Performance** : Requêtes optimisées, cache templates
- **Maintenabilité** : Code structuré, documentation complète
- **Évolutivité** : Architecture modulaire Django

### Tests et Validation

#### Fonctionnalités Testées ✅
- **Création de produits** avec prix de base en euro
- **Ajout de prix négociés** avec contexte client
- **Sélection automatique des prix** lors des sorties AJAX
- **Calculs automatiques** : stock, valeurs, marges
- **Alertes de stock** : seuils et notifications
- **Export CSV** avec données en euro
- **Interface ukrainienne** complète
- **Design responsive** sur mobile/desktop

#### Points de Contrôle
1. **Montants en euro** : Tous les prix affichés avec le symbole €
2. **Prix négociés** : Sélection dynamique lors des sorties
3. **Calculs** : Précision décimale et cohérence des totaux
4. **Interface** : Traduction ukrainienne complète
5. **Navigation** : Liens et formulaires fonctionnels

### Architecture Technique

L'application respecte les bonnes pratiques Django :
- **Modèles** : Séparation claire des données (Produit, Mouvement, PrixVente)
- **Vues** : Logique métier centralisée avec gestion d'erreurs
- **Templates** : Interface cohérente avec Bootstrap 5
- **URLs** : Structure RESTful et URLs parlantes
- **Formulaires** : Validation côté serveur et client
- **AJAX** : Interactions dynamiques pour l'UX

Pour toute question ou amélioration, référez-vous au code source dans le dossier `inventory/` qui contient toute la logique métier.
