# Gestion des Entrées/Sorties de Marchandises — Application Django

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

## Contraintes techniques

- **Framework** : Django (Python)
- **Base de données** : SQLite (par défaut)
- **Front-end** : Django templates + Bootstrap (ou TailwindCSS)
- **Déploiement local** : compatible VSCode, `python manage.py runserver`
- **Langue de l’interface** : ukrainien (tous les textes affichés à l’utilisateur doivent être traduits en ukrainien)

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

## Style de code et bonnes pratiques

- Code structuré, commenté en français
- Simplicité, clarté, efficacité
- Utilisation des conventions Django
- Fichiers README et requirements.txt à générer

---

**Instructions Copilot** :  
Itérer étape par étape, valider chaque fonctionnalité avant de passer à la suivante. Générer le code en respectant la structure et les contraintes ci-dessus.  
**Veiller à ce que toute l’interface utilisateur soit en ukrainien** (même pour les messages d’erreur et les intitulés de champs).