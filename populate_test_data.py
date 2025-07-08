#!/usr/bin/env python
"""
Script pour populer l'application avec des données de test
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockmanager.settings')
django.setup()

from inventory.models import Produit, PrixVente, Mouvement
from decimal import Decimal

def create_test_data():
    """Créer des données de test"""
    
    # Créer des produits
    produit1 = Produit.objects.create(
        nom="Ordinateur portable Dell",
        description="Ordinateur portable Dell Inspiron 15 pouces",
        cout_achat=Decimal('800.00'),
        prix_vente=Decimal('1200.00'),
        seuil_alerte=5
    )
    
    produit2 = Produit.objects.create(
        nom="Souris sans fil Logitech",
        description="Souris sans fil Logitech MX Master 3",
        cout_achat=Decimal('45.00'),
        prix_vente=Decimal('75.00'),
        seuil_alerte=10
    )
    
    # Ajouter des prix négociés pour l'ordinateur
    prix1 = PrixVente.objects.create(
        produit=produit1,
        prix=Decimal('1100.00'),
        client="Entreprise TechCorp",
        commentaire="Remise volume (commande > 10 unités)",
        actif=True
    )
    
    prix2 = PrixVente.objects.create(
        produit=produit1,
        prix=Decimal('1150.00'),
        client="Client fidèle Jean Dupont",
        commentaire="Remise fidélité",
        actif=True
    )
    
    # Ajouter un prix négocié pour la souris
    prix3 = PrixVente.objects.create(
        produit=produit2,
        prix=Decimal('65.00'),
        client="Revendeur ABC",
        commentaire="Prix revendeur",
        actif=True
    )
    
    # Ajouter des mouvements d'entrée
    Mouvement.objects.create(
        produit=produit1,
        type_mouvement='entree',
        quantite=20,
        commentaire="Réception livraison fournisseur"
    )
    
    Mouvement.objects.create(
        produit=produit2,
        type_mouvement='entree',
        quantite=50,
        commentaire="Réception stock initial"
    )
    
    # Ajouter des mouvements de sortie avec prix négociés
    Mouvement.objects.create(
        produit=produit1,
        type_mouvement='sortie',
        quantite=3,
        prix_vente_utilise=prix1,  # Prix négocié entreprise
        commentaire="Vente Entreprise TechCorp"
    )
    
    Mouvement.objects.create(
        produit=produit2,
        type_mouvement='sortie',
        quantite=5,
        prix_vente_utilise=prix3,  # Prix revendeur
        commentaire="Vente Revendeur ABC"
    )
    
    print("✅ Données de test créées avec succès !")
    print(f"📦 Produit 1: {produit1.nom} - Stock: {produit1.stock_actuel()} unités")
    print(f"📦 Produit 2: {produit2.nom} - Stock: {produit2.stock_actuel()} unités")
    print(f"💶 Prix négociés créés: {PrixVente.objects.count()} prix")
    print(f"📊 Mouvements créés: {Mouvement.objects.count()} mouvements")

if __name__ == '__main__':
    # Supprimer les données existantes (optionnel)
    print("🗑️  Suppression des données existantes...")
    Mouvement.objects.all().delete()
    PrixVente.objects.all().delete()
    Produit.objects.all().delete()
    
    # Créer les nouvelles données
    print("📦 Création des données de test...")
    create_test_data()
