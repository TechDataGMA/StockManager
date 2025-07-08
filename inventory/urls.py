from django.urls import path
from . import views

urlpatterns = [
    path('', views.tableau_bord, name='tableau_bord'),
    path('produits/', views.liste_produits, name='liste_produits'),
    path('produits/<int:pk>/', views.detail_produit, name='detail_produit'),
    path('produits/ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('produits/<int:pk>/modifier/', views.modifier_produit, 
         name='modifier_produit'),
    path('produits/<int:pk>/supprimer/', views.supprimer_produit, 
         name='supprimer_produit'),
    path('produits/<int:pk>/prix/ajouter/', views.ajouter_prix_vente, 
         name='ajouter_prix_vente'),
    path('produits/<int:pk>/prix/<int:prix_pk>/toggle/', views.toggle_prix_actif, 
         name='toggle_prix_actif'),
    path('mouvements/', views.liste_mouvements, name='liste_mouvements'),
    path('mouvements/ajouter/', views.ajouter_mouvement, 
         name='ajouter_mouvement'),
    path('mouvements/export/', views.export_mouvements_csv, 
         name='export_mouvements_csv'),
]
