# Gestion des Entrées/Sorties de Marchandises

Application Django complète pour la gestion des stocks avec interface en ukrainien.

## Fonctionnalités

### 🏪 Gestion des Produits
- ✅ Création, modification, suppression des produits
- ✅ Description, coût d'achat, prix de vente
- ✅ Seuil d'alerte personnalisable
- ✅ Calcul automatique du stock actuel
- ✅ Valeur du stock en cours

### 📊 Tableau de Bord
- ✅ Vue d'ensemble des stocks
- ✅ Statistiques générales
- ✅ Alertes de stock faible/épuisé
- ✅ Historique des derniers mouvements
- ✅ Indicateurs visuels colorés

### 📈 Gestion des Mouvements
- ✅ Enregistrement des entrées/sorties
- ✅ Historique complet avec filtres
- ✅ Filtrage par date, type, produit
- ✅ Export CSV des données
- ✅ Commentaires sur les opérations

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

### 📁 Export et Rapports
- ✅ Export CSV des mouvements
- ✅ Filtres avancés
- ✅ Historique détaillé

## Installation

1. Créer un environnement virtuel :
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\activate  # Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Effectuer les migrations :
```bash
python manage.py makemigrations
python manage.py migrate
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

## Technologies Utilisées

- **Backend**: Django 5.2.4
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Base de données**: SQLite (par défaut)
- **Langue**: Interface en ukrainien
- **CSS Framework**: Bootstrap 5.3.0
