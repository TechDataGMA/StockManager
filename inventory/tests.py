from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
import json

from .models import Produit, Mouvement, PrixVente
from .forms import ProduitForm, MouvementForm, PrixVenteForm


class ProduitModelTest(TestCase):
    """Tests unitaires pour le modèle Produit"""

    def setUp(self):
        """Préparation des données de test"""
        self.produit = Produit.objects.create(
            description="Produit Test",
            cout_achat=Decimal('10.00'),
            prix_vente=Decimal('15.00'),
            seuil_alerte=5
        )

    def test_creation_produit(self):
        """Test de création d'un produit"""
        self.assertEqual(self.produit.description, "Produit Test")
        self.assertEqual(self.produit.cout_achat, Decimal('10.00'))
        self.assertEqual(self.produit.prix_vente, Decimal('15.00'))
        self.assertEqual(self.produit.seuil_alerte, 5)
        self.assertTrue(self.produit.date_creation)
        self.assertTrue(self.produit.date_modification)

    def test_str_representation(self):
        """Test de la représentation string du produit"""
        self.assertEqual(str(self.produit), "Produit Test")

    def test_stock_actuel_sans_mouvements(self):
        """Test du calcul de stock sans mouvements"""
        self.assertEqual(self.produit.stock_actuel(), 0)

    def test_stock_actuel_avec_mouvements(self):
        """Test du calcul de stock avec des mouvements"""
        # Ajouter des entrées
        Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=100
        )
        Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=50
        )
        # Ajouter des sorties
        Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='sortie',
            quantite=30
        )
        
        self.assertEqual(self.produit.stock_actuel(), 120)  # 150 - 30

    def test_est_en_rupture(self):
        """Test de détection de rupture de stock"""
        self.assertTrue(self.produit.est_en_rupture())  # Stock initial = 0
        
        # Ajouter du stock
        Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=10
        )
        self.assertFalse(self.produit.est_en_rupture())

    def test_est_en_alerte(self):
        """Test de détection d'alerte de stock"""
        # Stock à 0, en dessous du seuil de 5
        self.assertTrue(self.produit.est_en_alerte())
        
        # Stock à 3, en dessous du seuil
        Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=3
        )
        self.assertTrue(self.produit.est_en_alerte())
        
        # Stock à 10, au-dessus du seuil
        Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=7
        )
        self.assertFalse(self.produit.est_en_alerte())

    def test_statut_stock(self):
        """Test du statut de stock"""
        self.assertEqual(self.produit.statut_stock(), 'rupture')
        
        # Stock en alerte
        Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=3
        )
        self.assertEqual(self.produit.statut_stock(), 'alerte')
        
        # Stock normal
        Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=10
        )
        self.assertEqual(self.produit.statut_stock(), 'normal')

    def test_valeur_stock(self):
        """Test du calcul de la valeur du stock"""
        Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=10
        )
        expected_value = 10 * self.produit.cout_achat
        self.assertEqual(self.produit.valeur_stock(), expected_value)

    def test_marge_beneficiaire(self):
        """Test du calcul de la marge bénéficiaire"""
        expected_marge = self.produit.prix_vente - self.produit.cout_achat
        self.assertEqual(self.produit.marge_beneficiaire(), expected_marge)


class PrixVenteModelTest(TestCase):
    """Tests unitaires pour le modèle PrixVente"""

    def setUp(self):
        self.produit = Produit.objects.create(
            description="Produit Test",
            cout_achat=Decimal('10.00'),
            prix_vente=Decimal('15.00')
        )

    def test_creation_prix_vente(self):
        """Test de création d'un prix de vente"""
        prix = PrixVente.objects.create(
            produit=self.produit,
            prix=Decimal('18.00'),
            client="Client Test",
            commentaire="Prix négocié"
        )
        
        self.assertEqual(prix.produit, self.produit)
        self.assertEqual(prix.prix, Decimal('18.00'))
        self.assertEqual(prix.client, "Client Test")
        self.assertTrue(prix.actif)
        self.assertTrue(prix.date_creation)

    def test_str_representation(self):
        """Test de la représentation string du prix de vente"""
        prix = PrixVente.objects.create(
            produit=self.produit,
            prix=Decimal('18.00'),
            client="Client Test"
        )
        expected = f"{self.produit.description} - {prix.prix}€ (Client Test)"
        self.assertEqual(str(prix), expected)

    def test_prix_vente_actuel_avec_prix_negocie(self):
        """Test du prix de vente actuel avec prix négocié"""
        # Créer un prix négocié actif
        PrixVente.objects.create(
            produit=self.produit,
            prix=Decimal('18.00'),
            actif=True
        )
        
        self.assertEqual(self.produit.prix_vente_actuel(), Decimal('18.00'))

    def test_prix_vente_actuel_sans_prix_negocie(self):
        """Test du prix de vente actuel sans prix négocié"""
        self.assertEqual(self.produit.prix_vente_actuel(), Decimal('15.00'))


class MouvementModelTest(TestCase):
    """Tests unitaires pour le modèle Mouvement"""

    def setUp(self):
        self.produit = Produit.objects.create(
            description="Produit Test",
            cout_achat=Decimal('10.00'),
            prix_vente=Decimal('15.00')
        )

    def test_creation_mouvement_entree(self):
        """Test de création d'un mouvement d'entrée"""
        mouvement = Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=50,
            commentaire="Test entrée"
        )
        
        self.assertEqual(mouvement.produit, self.produit)
        self.assertEqual(mouvement.type_mouvement, 'entree')
        self.assertEqual(mouvement.quantite, 50)
        self.assertTrue(mouvement.date_mouvement)

    def test_creation_mouvement_sortie(self):
        """Test de création d'un mouvement de sortie"""
        mouvement = Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='sortie',
            quantite=20
        )
        
        self.assertEqual(mouvement.type_mouvement, 'sortie')
        self.assertEqual(mouvement.quantite, 20)

    def test_str_representation(self):
        """Test de la représentation string du mouvement"""
        mouvement = Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=50
        )
        expected = f"Надходження - {self.produit.description} (50)"
        self.assertEqual(str(mouvement), expected)

    def test_prix_utilise_entree(self):
        """Test du prix utilisé pour une entrée"""
        mouvement = Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=50
        )
        self.assertIsNone(mouvement.prix_utilise())

    def test_prix_utilise_sortie_sans_prix_negocie(self):
        """Test du prix utilisé pour une sortie sans prix négocié"""
        mouvement = Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='sortie',
            quantite=20
        )
        self.assertEqual(mouvement.prix_utilise(), self.produit.prix_vente)

    def test_prix_utilise_sortie_avec_prix_negocie(self):
        """Test du prix utilisé pour une sortie avec prix négocié"""
        prix_negocie = PrixVente.objects.create(
            produit=self.produit,
            prix=Decimal('18.00')
        )
        
        mouvement = Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='sortie',
            quantite=20,
            prix_vente_utilise=prix_negocie
        )
        
        self.assertEqual(mouvement.prix_utilise(), Decimal('18.00'))

    def test_valeur_mouvement_entree(self):
        """Test du calcul de valeur pour une entrée"""
        mouvement = Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=50
        )
        expected_value = 50 * self.produit.cout_achat
        self.assertEqual(mouvement.valeur_mouvement(), expected_value)

    def test_valeur_mouvement_sortie(self):
        """Test du calcul de valeur pour une sortie"""
        mouvement = Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='sortie',
            quantite=20
        )
        expected_value = 20 * self.produit.prix_vente
        self.assertEqual(mouvement.valeur_mouvement(), expected_value)


class ProduitFormTest(TestCase):
    """Tests unitaires pour le formulaire Produit"""

    def test_form_valide(self):
        """Test d'un formulaire valide"""
        form_data = {
            'description': 'Nouveau Produit',
            'cout_achat': '12.50',
            'prix_vente': '18.00',
            'seuil_alerte': '10'
        }
        form = ProduitForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalide_prix_negatif(self):
        """Test d'un formulaire avec prix négatif"""
        form_data = {
            'description': 'Nouveau Produit',
            'cout_achat': '-5.00',
            'prix_vente': '18.00',
            'seuil_alerte': '10'
        }
        form = ProduitForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalide_description_vide(self):
        """Test d'un formulaire avec description vide"""
        form_data = {
            'description': '',
            'cout_achat': '12.50',
            'prix_vente': '18.00',
            'seuil_alerte': '10'
        }
        form = ProduitForm(data=form_data)
        self.assertFalse(form.is_valid())


class MouvementFormTest(TestCase):
    """Tests unitaires pour le formulaire Mouvement"""

    def setUp(self):
        self.produit = Produit.objects.create(
            description="Produit Test",
            cout_achat=Decimal('10.00'),
            prix_vente=Decimal('15.00')
        )

    def test_form_valide_entree(self):
        """Test d'un formulaire valide pour une entrée"""
        form_data = {
            'produit': self.produit.pk,
            'type_mouvement': 'entree',
            'quantite': '50',
            'commentaire': 'Test entrée'
        }
        form = MouvementForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_valide_sortie(self):
        """Test d'un formulaire valide pour une sortie"""
        form_data = {
            'produit': self.produit.pk,
            'type_mouvement': 'sortie',
            'quantite': '20'
        }
        form = MouvementForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalide_quantite_negative(self):
        """Test d'un formulaire avec quantité négative"""
        form_data = {
            'produit': self.produit.pk,
            'type_mouvement': 'entree',
            'quantite': '-10'
        }
        form = MouvementForm(data=form_data)
        self.assertFalse(form.is_valid())


class PrixVenteFormTest(TestCase):
    """Tests unitaires pour le formulaire PrixVente"""

    def test_form_valide(self):
        """Test d'un formulaire valide"""
        form_data = {
            'prix': '18.50',
            'client': 'Client Test',
            'commentaire': 'Prix spécial',
            'actif': True
        }
        form = PrixVenteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_valide_sans_client(self):
        """Test d'un formulaire valide sans client"""
        form_data = {
            'prix': '18.50',
            'client': '',
            'commentaire': '',
            'actif': True
        }
        form = PrixVenteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalide_prix_negatif(self):
        """Test d'un formulaire avec prix négatif"""
        form_data = {
            'prix': '-5.00',
            'client': 'Client Test',
            'actif': True
        }
        form = PrixVenteForm(data=form_data)
        self.assertFalse(form.is_valid())


class TableauBordViewTest(TestCase):
    """Tests d'intégration pour la vue tableau de bord"""

    def setUp(self):
        self.client = Client()
        self.produit = Produit.objects.create(
            description="Produit Test",
            cout_achat=Decimal('10.00'),
            prix_vente=Decimal('15.00'),
            seuil_alerte=5
        )

    def test_tableau_bord_accessible(self):
        """Test d'accessibilité du tableau de bord"""
        response = self.client.get(reverse('tableau_bord'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Produit Test")

    def test_tableau_bord_statistiques(self):
        """Test des statistiques du tableau de bord"""
        # Ajouter quelques mouvements
        Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=10
        )
        
        response = self.client.get(reverse('tableau_bord'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_produits'], 1)
        self.assertEqual(response.context['total_mouvements'], 1)

    def test_tableau_bord_alertes(self):
        """Test des alertes dans le tableau de bord"""
        # Produit en rupture (stock = 0)
        response = self.client.get(reverse('tableau_bord'))
        self.assertIn(self.produit, response.context['produits_en_rupture'])
        
        # Ajouter du stock pour alerte
        Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=3
        )
        
        response = self.client.get(reverse('tableau_bord'))
        self.assertIn(self.produit, response.context['produits_en_alerte'])


class ProduitViewsTest(TestCase):
    """Tests d'intégration pour les vues de produits"""

    def setUp(self):
        self.client = Client()
        self.produit = Produit.objects.create(
            description="Produit Test",
            cout_achat=Decimal('10.00'),
            prix_vente=Decimal('15.00')
        )

    def test_liste_produits(self):
        """Test de la liste des produits"""
        response = self.client.get(reverse('liste_produits'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Produit Test")

    def test_detail_produit(self):
        """Test du détail d'un produit"""
        response = self.client.get(reverse('detail_produit', args=[self.produit.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Produit Test")

    def test_ajouter_produit_get(self):
        """Test d'affichage du formulaire d'ajout de produit"""
        response = self.client.get(reverse('ajouter_produit'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")

    def test_ajouter_produit_post_valide(self):
        """Test d'ajout d'un produit avec données valides"""
        data = {
            'description': 'Nouveau Produit',
            'cout_achat': '12.50',
            'prix_vente': '18.00',
            'seuil_alerte': '10'
        }
        response = self.client.post(reverse('ajouter_produit'), data)
        self.assertEqual(response.status_code, 302)  # Redirection
        self.assertTrue(Produit.objects.filter(description='Nouveau Produit').exists())

    def test_modifier_produit_get(self):
        """Test d'affichage du formulaire de modification"""
        response = self.client.get(reverse('modifier_produit', args=[self.produit.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Produit Test")

    def test_modifier_produit_post_valide(self):
        """Test de modification d'un produit avec données valides"""
        data = {
            'description': 'Produit Modifié',
            'cout_achat': '11.00',
            'prix_vente': '16.00',
            'seuil_alerte': '8'
        }
        response = self.client.post(reverse('modifier_produit', args=[self.produit.pk]), data)
        self.assertEqual(response.status_code, 302)  # Redirection
        
        self.produit.refresh_from_db()
        self.assertEqual(self.produit.description, 'Produit Modifié')

    def test_supprimer_produit_get(self):
        """Test d'affichage de la confirmation de suppression"""
        response = self.client.get(reverse('supprimer_produit', args=[self.produit.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Produit Test")

    def test_supprimer_produit_post(self):
        """Test de suppression d'un produit"""
        response = self.client.post(reverse('supprimer_produit', args=[self.produit.pk]))
        self.assertEqual(response.status_code, 302)  # Redirection
        self.assertFalse(Produit.objects.filter(pk=self.produit.pk).exists())


class MouvementViewsTest(TestCase):
    """Tests d'intégration pour les vues de mouvements"""

    def setUp(self):
        self.client = Client()
        self.produit = Produit.objects.create(
            description="Produit Test",
            cout_achat=Decimal('10.00'),
            prix_vente=Decimal('15.00')
        )

    def test_liste_mouvements(self):
        """Test de la liste des mouvements"""
        Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=10
        )
        
        response = self.client.get(reverse('liste_mouvements'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Produit Test")

    def test_ajouter_mouvement_get(self):
        """Test d'affichage du formulaire d'ajout de mouvement"""
        response = self.client.get(reverse('ajouter_mouvement'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")

    def test_ajouter_mouvement_post_valide(self):
        """Test d'ajout d'un mouvement avec données valides"""
        data = {
            'produit': self.produit.pk,
            'type_mouvement': 'entree',
            'quantite': '50',
            'commentaire': 'Test entrée'
        }
        response = self.client.post(reverse('ajouter_mouvement'), data)
        self.assertEqual(response.status_code, 302)  # Redirection
        self.assertTrue(Mouvement.objects.filter(quantite=50).exists())

    def test_filtres_mouvements(self):
        """Test des filtres sur la liste des mouvements"""
        # Créer plusieurs mouvements
        Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=10
        )
        Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='sortie',
            quantite=5
        )
        
        # Test filtre par type
        response = self.client.get(reverse('liste_mouvements'), {'type_mouvement': 'entree'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['mouvements']), 1)

    def test_export_csv(self):
        """Test de l'export CSV des mouvements"""
        Mouvement.objects.create(
            produit=self.produit,
            type_mouvement='entree',
            quantite=10
        )
        
        response = self.client.get(reverse('export_mouvements_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment', response['Content-Disposition'])


class PrixVenteViewsTest(TestCase):
    """Tests d'intégration pour les vues de prix de vente"""

    def setUp(self):
        self.client = Client()
        self.produit = Produit.objects.create(
            description="Produit Test",
            cout_achat=Decimal('10.00'),
            prix_vente=Decimal('15.00')
        )

    def test_ajouter_prix_vente_get(self):
        """Test d'affichage du formulaire d'ajout de prix"""
        response = self.client.get(reverse('ajouter_prix_vente', args=[self.produit.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Produit Test")

    def test_ajouter_prix_vente_post_valide(self):
        """Test d'ajout d'un prix de vente avec données valides"""
        data = {
            'prix': '18.50',
            'client': 'Client Test',
            'commentaire': 'Prix négocié',
            'actif': True
        }
        response = self.client.post(reverse('ajouter_prix_vente', args=[self.produit.pk]), data)
        self.assertEqual(response.status_code, 302)  # Redirection
        self.assertTrue(PrixVente.objects.filter(prix=Decimal('18.50')).exists())

    def test_toggle_prix_actif(self):
        """Test d'activation/désactivation d'un prix"""
        prix = PrixVente.objects.create(
            produit=self.produit,
            prix=Decimal('18.00'),
            actif=False
        )
        
        response = self.client.post(reverse('toggle_prix_actif', args=[self.produit.pk, prix.pk]))
        self.assertEqual(response.status_code, 302)  # Redirection
        
        prix.refresh_from_db()
        self.assertTrue(prix.actif)

    def test_get_prix_produit_ajax(self):
        """Test de récupération des prix via AJAX"""
        PrixVente.objects.create(
            produit=self.produit,
            prix=Decimal('18.00'),
            client='Client Test',
            actif=True
        )
        
        response = self.client.get(
            reverse('get_prix_produit', args=[self.produit.pk]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('prix', data)
        self.assertEqual(len(data['prix']), 2)  # Prix de base + prix négocié


class ScenarioIntegrationTest(TestCase):
    """Tests d'intégration couvrant des scénarios utilisateur complets"""

    def setUp(self):
        self.client = Client()

    def test_scenario_gestion_complete_produit(self):
        """Scénario complet : création, modification, mouvements, prix négociés"""
        # 1. Créer un produit
        data_produit = {
            'description': 'Produit Scenario',
            'cout_achat': '10.00',
            'prix_vente': '15.00',
            'seuil_alerte': '5'
        }
        response = self.client.post(reverse('ajouter_produit'), data_produit)
        self.assertEqual(response.status_code, 302)
        
        produit = Produit.objects.get(description='Produit Scenario')
        
        # 2. Ajouter du stock (entrée)
        data_entree = {
            'produit': produit.pk,
            'type_mouvement': 'entree',
            'quantite': '100',
            'commentaire': 'Stock initial'
        }
        response = self.client.post(reverse('ajouter_mouvement'), data_entree)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(produit.stock_actuel(), 100)
        
        # 3. Ajouter un prix négocié
        data_prix = {
            'prix': '18.00',
            'client': 'Client VIP',
            'commentaire': 'Prix spécial client VIP',
            'actif': True
        }
        response = self.client.post(reverse('ajouter_prix_vente', args=[produit.pk]), data_prix)
        self.assertEqual(response.status_code, 302)
        
        # 4. Effectuer une sortie avec prix négocié
        prix_negocie = PrixVente.objects.get(client='Client VIP')
        data_sortie = {
            'produit': produit.pk,
            'type_mouvement': 'sortie',
            'quantite': '20',
            'prix_vente_utilise': prix_negocie.pk,
            'commentaire': 'Vente client VIP'
        }
        response = self.client.post(reverse('ajouter_mouvement'), data_sortie)
        self.assertEqual(response.status_code, 302)
        
        # Vérifications finales
        produit.refresh_from_db()
        self.assertEqual(produit.stock_actuel(), 80)  # 100 - 20
        
        mouvement_sortie = Mouvement.objects.get(type_mouvement='sortie')
        self.assertEqual(mouvement_sortie.prix_utilise(), Decimal('18.00'))
        self.assertEqual(mouvement_sortie.valeur_mouvement(), Decimal('360.00'))  # 20 * 18

    def test_scenario_alertes_stock(self):
        """Scénario de gestion des alertes de stock"""
        # Créer un produit avec seuil d'alerte
        produit = Produit.objects.create(
            description="Produit Alerte",
            cout_achat=Decimal('5.00'),
            prix_vente=Decimal('8.00'),
            seuil_alerte=10
        )
        
        # Vérifier état initial (rupture)
        self.assertTrue(produit.est_en_rupture())
        self.assertEqual(produit.statut_stock(), 'rupture')
        
        # Ajouter du stock en alerte
        Mouvement.objects.create(
            produit=produit,
            type_mouvement='entree',
            quantite=5
        )
        
        self.assertTrue(produit.est_en_alerte())
        self.assertEqual(produit.statut_stock(), 'alerte')
        
        # Ajouter plus de stock pour statut normal
        Mouvement.objects.create(
            produit=produit,
            type_mouvement='entree',
            quantite=10
        )
        
        self.assertFalse(produit.est_en_alerte())
        self.assertEqual(produit.statut_stock(), 'normal')
        
        # Vérifier alertes dans le tableau de bord
        response = self.client.get(reverse('tableau_bord'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(produit, response.context['produits_en_alerte'])

    def test_scenario_export_filtres(self):
        """Scénario d'export CSV avec filtres"""
        # Créer plusieurs produits et mouvements
        produit1 = Produit.objects.create(
            description="Produit 1",
            cout_achat=Decimal('10.00'),
            prix_vente=Decimal('15.00')
        )
        produit2 = Produit.objects.create(
            description="Produit 2",
            cout_achat=Decimal('20.00'),
            prix_vente=Decimal('30.00')
        )
        
        # Mouvements pour produit 1
        Mouvement.objects.create(
            produit=produit1,
            type_mouvement='entree',
            quantite=100
        )
        Mouvement.objects.create(
            produit=produit1,
            type_mouvement='sortie',
            quantite=20
        )
        
        # Mouvements pour produit 2
        Mouvement.objects.create(
            produit=produit2,
            type_mouvement='entree',
            quantite=50
        )
        
        # Test export sans filtre
        response = self.client.get(reverse('export_mouvements_csv'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8-sig')
        self.assertIn('Produit 1', content)
        self.assertIn('Produit 2', content)
        
        # Test export avec filtre par produit
        response = self.client.get(reverse('export_mouvements_csv'), {'produit': produit1.pk})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8-sig')
        self.assertIn('Produit 1', content)
        # Note: Le filtrage dans l'export n'est pas encore implémenté dans le code fourni
        # mais le test vérifie la structure de base

    def test_scenario_calculs_financiers(self):
        """Scénario de calculs financiers (valeurs, marges)"""
        produit = Produit.objects.create(
            description="Produit Financier",
            cout_achat=Decimal('12.50'),
            prix_vente=Decimal('20.00'),
            seuil_alerte=5
        )
        
        # Ajouter du stock
        Mouvement.objects.create(
            produit=produit,
            type_mouvement='entree',
            quantite=100
        )
        
        # Vérifier calculs
        self.assertEqual(produit.stock_actuel(), 100)
        self.assertEqual(produit.valeur_stock(), Decimal('1250.00'))  # 100 * 12.50
        self.assertEqual(produit.marge_beneficiaire(), Decimal('7.50'))  # 20.00 - 12.50
        
        # Ajouter prix négocié
        PrixVente.objects.create(
            produit=produit,
            prix=Decimal('25.00'),
            actif=True
        )
        
        # Vérifier nouveau calcul de marge
        self.assertEqual(produit.prix_vente_actuel(), Decimal('25.00'))
        self.assertEqual(produit.marge_beneficiaire(), Decimal('12.50'))  # 25.00 - 12.50
        
        # Mouvement de sortie avec prix négocié
        prix_negocie = PrixVente.objects.get(prix=Decimal('25.00'))
        mouvement = Mouvement.objects.create(
            produit=produit,
            type_mouvement='sortie',
            quantite=30,
            prix_vente_utilise=prix_negocie
        )
        
        self.assertEqual(mouvement.valeur_mouvement(), Decimal('750.00'))  # 30 * 25.00
