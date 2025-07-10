# Gestion de### 1. Gestion des produits
- Ajouter, modifier, supprimer un produit
- Champ descr- **Tests d'intégration** :  
  Couvrir les principaux scénarios utilisateurs (création de produit, enregistrement d'un mouvement, sélection d'un prix négocié, export CSV, alertes, upload de photos, gestion des coûts variables).tion, coût d'achat, prix de vente
- **Gestion des photos de produits** : Upload et affichage d'images pour chaque produit
- **Coûts d'achat variables** : Historique des coûts d'achat selon les fournisseurs et contextesntrées/Sorties de Marchandises — Application Django

## Objectif

Développer une application web légère sous Django permettant de gérer les entrées et sorties de marchandises, incluant :
- Gestion des produits (description, coût d'achat, prix de vente)
- Suivi des mouvements (entrées, sorties) avec historique
- Interface web simple pour CRUD (Créer, Lire, Mettre à jour, Supprimer)
- Interface utilisateur compacte et responsive

## Fonctionnalités attendues

### 1. Gestion des produits
- Ajouter, modifier, supprimer un produit
- Champ description, coût d’achat, prix de vente

### 2. Suivi des mouvements de stock
- Enregistrer une entrée ou une sortie de produit
- Choisir le produit concerné
- Quantité, date, commentaire optionnel
- Affichage de l’historique des mouvements

### 3. Tableau de bord
- Visualisation du stock courant pour chaque produit
- Historique des opérations

### 4. Interface web
- Navigation simple et claire
- Formulaires pour chaque opération
- Utilisation de Django templates (Bootstrap ou équivalent léger)
- **Toute l’interface (titres, boutons, labels, messages) doit être en ukrainien**  
  (utiliser la traduction ukrainienne pour tous les textes visibles par l’utilisateur)

## Fonctionnalités avancées (extension Copilot)

### Gestion avancée des prix de vente
- Un produit peut avoir plusieurs prix négociés (par client ou contexte)
- Historique complet des prix négociés, avec date, client, commentaire, statut actif/inactif
- Lors d'une sortie, l'utilisateur choisit le prix négocié à appliquer (prix de base ou prix négocié actif)
- Sélection dynamique du prix via AJAX selon le produit choisi
- Tous les montants sont affichés et exportés en euro (€)
- Calcul automatique de la valeur du mouvement selon le prix sélectionné
- Marge bénéficiaire calculée automatiquement

### Gestion des photos de produits
- Upload d'images pour chaque produit (formats JPG, PNG, GIF)
- Affichage des photos dans la liste des produits (miniatures)
- Affichage des photos dans le détail du produit (image complète)
- Gestion du formulaire avec `enctype="multipart/form-data"`
- Stockage des images dans le dossier `media/produits/`
- Affichage conditionnel (placeholder si pas de photo)

### Gestion des coûts d'achat variables
- Historique complet des coûts d'achat par produit
- Coût par fournisseur ou contexte d'achat
- Système d'activation/désactivation des coûts
- Sélection dynamique du coût lors des mouvements d'entrée
- Calcul automatique de la valeur des mouvements selon le coût sélectionné
- Interface de gestion complète (ajout, activation, historique)
- Intégration AJAX pour la sélection en temps réel

### Interface et expérience utilisateur
- Interface 100% en ukrainien (labels, messages, erreurs, boutons)
- Design responsive et moderne avec Bootstrap 5
- Navigation intuitive, feedback utilisateur, icônes

### Filtres, alertes et export
- Filtres avancés sur les mouvements (date, type, produit)
- Système d'alertes visuelles (stock bas, rupture)
- Export CSV des mouvements filtrés, avec montants en euro

### Architecture technique
- Modèles : Produit, Mouvement, PrixVente (historique des prix), CoutAchat (historique des coûts)
- Gestion des fichiers media pour les photos de produits
- Formulaires adaptés pour la gestion des prix négociés et coûts variables avec sélection lors des mouvements
- Vues Django avec gestion AJAX pour la sélection dynamique des prix et coûts
- Templates Bootstrap avec affichage des photos, prix négociés, coûts variables et montants en euro
- Code et documentation en français, interface utilisateur en ukrainien

## Contraintes techniques

- **Framework** : Django (Python)
- **Base de données** : SQLite (par défaut)
- **Front-end** : Django templates + Bootstrap (ou TailwindCSS)
- **Déploiement local** : compatible VSCode, `python manage.py runserver`
- **Langue de l’interface** : ukrainien (tous les textes affichés à l’utilisateur doivent être traduits en ukrainien)

### Qualité & Tests

- **Tests unitaires** :  
  Rédiger des tests unitaires pour chaque modèle, vue et fonction métier critique.
- **Tests d’intégration** :  
  Couvrir les principaux scénarios utilisateurs (création de produit, enregistrement d’un mouvement, sélection d’un prix négocié, export CSV, alertes).
- **Outils** :  
  Utiliser le framework de test Django (`django.test`) et `pytest` si besoin.
- **Livrables** :  
  Les tests doivent être placés dans des fichiers `tests.py` ou sous un répertoire `tests/`, bien structurés et commentés en français.
- **Couverture** :  
  Viser une couverture de code d’au moins 80% sur les fonctionnalités métier.
- **Exécution** :  
  Les tests doivent pouvoir être lancés via `python manage.py test`.

## Déroulement suggéré pour GitHub Copilot

1. **Initialisation du projet Django**
   - Création du projet et de l’application principale

2. **Définition des modèles**
   - Modèles Produit et Mouvement

3. **Création de l’admin Django**
   - Configuration minimale pour gérer produits et mouvements

4. **Création des vues et templates**
   - Listes, formulaires de création/édition/suppression
   - Tableau de bord

5. **Gestion du stock courant**
   - Calcul dynamique (entrées - sorties) pour chaque produit

6. **Améliorations optionnelles**
   - Ajout d’un filtre par dates
   - Export CSV de l’historique
   - Authentification basique (facultatif)

---

**Instructions Copilot** :  
Itérer étape par étape, valider chaque fonctionnalité avant de passer à la suivante. Générer le code en respectant la structure et les contraintes ci-dessus.  
**Veiller à ce que toute l’interface utilisateur soit en ukrainien** (même pour les messages d’erreur et les intitulés de champs).