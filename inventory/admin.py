from django.contrib import admin
from .models import Produit, Mouvement


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    """Administration des produits"""
    list_display = ['description', 'cout_achat', 'prix_vente', 'seuil_alerte', 'stock_actuel', 'statut_stock']
    search_fields = ['description']
    list_filter = ['date_creation', 'seuil_alerte']
    readonly_fields = ['date_creation', 'date_modification']
    
    def statut_stock(self, obj):
        """Affiche le statut du stock avec couleur"""
        statut = obj.statut_stock()
        colors = {
            'normal': 'green',
            'alerte': 'orange', 
            'rupture': 'red'
        }
        return f'<span style="color: {colors[statut]}">{statut.title()}</span>'
    
    statut_stock.allow_tags = True
    statut_stock.short_description = 'Статус запасу'


@admin.register(Mouvement)
class MouvementAdmin(admin.ModelAdmin):
    """Administration des mouvements"""
    list_display = ['produit', 'type_mouvement', 'quantite', 'date_mouvement']
    list_filter = ['type_mouvement', 'date_mouvement']
    search_fields = ['produit__description', 'commentaire']
    readonly_fields = ['date_mouvement']
