# Nouvelles Fonctionnalités - Photos et Coûts d'Achat Variables

## 📋 Vue d'ensemble

Ce document décrit les deux nouvelles fonctionnalités ajoutées au système de gestion de stock :

1. **Gestion des photos de produits**
2. **Gestion des coûts d'achat variables**

## 📸 Gestion des Photos de Produits

### Fonctionnalités

- **Upload de photos** : Formats supportés JPG, PNG, GIF (max 5MB)
- **Affichage miniatures** : Dans la liste des produits
- **Affichage complet** : Dans la page de détail du produit
- **Placeholder** : Icône par défaut si pas de photo
- **Stockage** : Dans le dossier `media/produits/`

### Configuration Technique

```python
# Dans models.py
photo = models.ImageField(
    upload_to='produits/',
    blank=True,
    null=True,
    verbose_name="Фото товару",
    help_text="Зображення товару"
)
```

### URLs Media

Les fichiers sont servis via :
- **Développement** : `http://localhost:8000/media/produits/nom_fichier.jpg`
- **Production** : Configuration via serveur web (nginx/apache)

### Templates

- **Formulaire** : `enctype="multipart/form-data"` requis
- **Liste** : Miniatures 50x50px avec fallback
- **Détail** : Image responsive max-height 300px

## 💰 Gestion des Coûts d'Achat Variables

### Fonctionnalités

- **Historique complet** : Tous les coûts d'achat par produit
- **Contexte fournisseur** : Associer un coût à un fournisseur
- **Système d'activation** : Un seul coût actif à la fois
- **Sélection dynamique** : AJAX lors des mouvements d'entrée
- **Calculs automatiques** : Valeur stock et mouvements

### Modèle CoutAchat

```python
class CoutAchat(models.Model):
    produit = models.ForeignKey(Produit, related_name='cout_achat_historique')
    cout = models.DecimalField(max_digits=10, decimal_places=2)
    fournisseur = models.CharField(max_length=200, blank=True)
    actif = models.BooleanField(default=True)
    commentaire = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
```

### Intégration avec les Mouvements

- **Entrées** : Sélection du coût d'achat à appliquer
- **Calculs** : Valeur = quantité × coût sélectionné
- **Historique** : Traçabilité du coût utilisé

### Interface Utilisateur

- **Liste des coûts** : Dans la page détail produit
- **Formulaire d'ajout** : Page dédiée avec validation
- **Actions** : Activer/désactiver avec confirmation
- **AJAX** : Chargement dynamique selon le produit

## 🔧 Installation et Configuration

### 1. Prérequis

```bash
# Installer Pillow pour la gestion d'images
pip install Pillow
```

### 2. Migrations

```bash
# Appliquer les migrations
python manage.py migrate
```

### 3. Configuration Media

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

```python
# urls.py principal
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 4. Dossier Media

```bash
# Créer le dossier media
mkdir -p media/produits
chmod 755 media/produits
```

## 🧪 Tests

### Exécution des Tests

```bash
# Tests spécifiques aux nouvelles fonctionnalités
python manage.py test inventory.tests.PhotoProduitTest
python manage.py test inventory.tests.CoutAchatTest
python manage.py test inventory.tests.IntegrationPhotoEtCoutTest

# Script de test complet
./test_nouvelles_fonctionnalites.sh
```

### Tests Couverts

1. **Photos** :
   - Upload de fichiers
   - Affichage avec/sans photo
   - Validation des formats

2. **Coûts d'achat** :
   - Création et gestion
   - Activation/désactivation
   - Calculs de valeurs
   - Intégration AJAX

3. **Intégration** :
   - Workflow complet
   - Calculs combinés
   - Scénarios multiples

## 📱 Utilisation

### Ajouter une Photo à un Produit

1. Aller dans "Список товарів"
2. Cliquer sur "Редагувати" pour un produit
3. Utiliser le champ "Фото товару"
4. Sélectionner un fichier image
5. Sauvegarder

### Gérer les Coûts d'Achat

1. Aller dans le détail d'un produit
2. Section "Собівартості"
3. Cliquer "Додати собівартість"
4. Remplir le formulaire (coût, fournisseur, commentaire)
5. Cocher "Активна" si nécessaire
6. Sauvegarder

### Créer un Mouvement avec Coût Spécifique

1. "Додати рух товару"
2. Sélectionner produit et type "Надходження"
3. Le champ coût d'achat apparaît automatiquement
4. Choisir le coût à appliquer
5. Saisir quantité et commentaire
6. Enregistrer

## 🐛 Dépannage

### Problèmes Courants

1. **Photos ne s'affichent pas** :
   - Vérifier MEDIA_URL et MEDIA_ROOT
   - Vérifier les permissions du dossier media
   - Vérifier la configuration URLs

2. **Upload échoue** :
   - Vérifier la taille du fichier (< 5MB)
   - Vérifier le format (JPG, PNG, GIF)
   - Vérifier l'espace disque

3. **AJAX ne fonctionne pas** :
   - Vérifier les URLs des endpoints
   - Vérifier la console JavaScript
   - Vérifier les headers X-Requested-With

### Logs

```bash
# Vérifier les logs d'erreur
tail -f logs/prod.txt

# Mode debug
DEBUG = True  # dans settings.py
```

## 🚀 Fonctionnalités Futures

### Améliorations Possibles

1. **Photos** :
   - Galerie multi-photos
   - Redimensionnement automatique
   - Watermarking
   - Compression

2. **Coûts** :
   - Import en masse
   - Notifications de changement
   - Historique des prix fournisseurs
   - Statistiques de coûts

3. **Interface** :
   - Drag & drop photos
   - Prévisualisation en temps réel
   - Calculatrice de marge
   - Export des coûts

## 📞 Support

Pour toute question ou problème :

1. Consulter les tests unitaires
2. Vérifier la documentation SPEC.md
3. Examiner les logs d'application
4. Tester en mode debug
