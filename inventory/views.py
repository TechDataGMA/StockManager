from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Produit, Mouvement, PrixVente
from .forms import ProduitForm, MouvementForm, FiltreMovementForm, PrixVenteForm
import csv
from django.http import HttpResponse, JsonResponse


def tableau_bord(request):
    """Vue du tableau de bord principal"""
    produits = Produit.objects.all()
    mouvements_recents = Mouvement.objects.select_related('produit')[:10]
    
    # Statistiques
    total_produits = produits.count()
    total_mouvements = Mouvement.objects.count()
    
    # Alertes de stock
    produits_en_rupture = [p for p in produits if p.est_en_rupture()]
    produits_en_alerte = [p for p in produits if p.est_en_alerte() and not p.est_en_rupture()]
    
    # Valeur totale du stock
    valeur_totale_stock = sum(p.valeur_stock() for p in produits)
    
    context = {
        'produits': produits,
        'mouvements_recents': mouvements_recents,
        'total_produits': total_produits,
        'total_mouvements': total_mouvements,
        'produits_en_rupture': produits_en_rupture,
        'produits_en_alerte': produits_en_alerte,
        'valeur_totale_stock': valeur_totale_stock,
    }
    return render(request, 'inventory/tableau_bord.html', context)


def liste_produits(request):
    """Liste de tous les produits"""
    produits = Produit.objects.all()
    return render(request, 'inventory/liste_produits.html', 
                  {'produits': produits})


def detail_produit(request, pk):
    """Détail d'un produit avec ses mouvements et prix de vente"""
    produit = get_object_or_404(Produit, pk=pk)
    mouvements = produit.mouvement_set.all()
    prix_historique = produit.prix_vente_historique.all()
    return render(request, 'inventory/detail_produit.html', {
        'produit': produit,
        'mouvements': mouvements,
        'prix_historique': prix_historique
    })


def ajouter_produit(request):
    """Ajouter un nouveau produit"""
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успішно додано!')
            return redirect('liste_produits')
    else:
        form = ProduitForm()
    return render(request, 'inventory/form_produit.html', 
                  {'form': form, 'title': 'Додати товар'})


def modifier_produit(request, pk):
    """Modifier un produit existant"""
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успішно оновлено!')
            return redirect('detail_produit', pk=produit.pk)
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'inventory/form_produit.html', {
        'form': form,
        'title': 'Редагувати товар',
        'produit': produit
    })


def supprimer_produit(request, pk):
    """Supprimer un produit"""
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        produit.delete()
        messages.success(request, 'Товар успішно видалено!')
        return redirect('liste_produits')
    return render(request, 'inventory/confirmer_suppression.html', 
                  {'produit': produit})


def liste_mouvements(request):
    """Liste de tous les mouvements avec filtres"""
    mouvements = Mouvement.objects.select_related('produit').all()
    form = FiltreMovementForm(request.GET)
    
    if form.is_valid():
        # Filtrage par date de début
        if form.cleaned_data['date_debut']:
            mouvements = mouvements.filter(
                date_mouvement__date__gte=form.cleaned_data['date_debut']
            )
        
        # Filtrage par date de fin
        if form.cleaned_data['date_fin']:
            mouvements = mouvements.filter(
                date_mouvement__date__lte=form.cleaned_data['date_fin']
            )
        
        # Filtrage par type de mouvement
        if form.cleaned_data['type_mouvement']:
            mouvements = mouvements.filter(
                type_mouvement=form.cleaned_data['type_mouvement']
            )
        
        # Filtrage par produit
        if form.cleaned_data['produit']:
            mouvements = mouvements.filter(
                produit=form.cleaned_data['produit']
            )
    
    context = {
        'mouvements': mouvements,
        'form': form,
        'total_mouvements': mouvements.count(),
    }
    return render(request, 'inventory/liste_mouvements.html', context)


def ajouter_mouvement(request):
    """Ajouter un nouveau mouvement"""
    if request.method == 'POST':
        form = MouvementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Рух товару успішно зареєстровано!')
            return redirect('liste_mouvements')
    else:
        form = MouvementForm()
    return render(request, 'inventory/form_mouvement.html', 
                  {'form': form, 'title': 'Додати рух товару'})

def export_mouvements_csv(request):
    """Exporter les mouvements en CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mouvements.csv"'
    response.write('\ufeff')  # BOM pour Excel

    writer = csv.writer(response)
    writer.writerow([
        'Дата', 'Товар', 'Тип операції', 'Кількість', 'Коментар'
    ])

    mouvements = Mouvement.objects.select_related('produit').all()
    
    # Appliquer les mêmes filtres que la liste
    form = FiltreMovementForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['date_debut']:
            mouvements = mouvements.filter(
                date_mouvement__date__gte=form.cleaned_data['date_debut']
            )
        if form.cleaned_data['date_fin']:
            mouvements = mouvements.filter(
                date_mouvement__date__lte=form.cleaned_data['date_fin']
            )
        if form.cleaned_data['type_mouvement']:
            mouvements = mouvements.filter(
                type_mouvement=form.cleaned_data['type_mouvement']
            )
        if form.cleaned_data['produit']:
            mouvements = mouvements.filter(
                produit=form.cleaned_data['produit']
            )

    for mouvement in mouvements:
        writer.writerow([
            mouvement.date_mouvement.strftime('%d.%m.%Y %H:%M'),
            mouvement.produit.description,
            mouvement.get_type_mouvement_display(),
            mouvement.quantite,
            mouvement.commentaire or ''
        ])

    return response


def ajouter_prix_vente(request, pk):
    """Ajouter un nouveau prix de vente pour un produit"""
    produit = get_object_or_404(Produit, pk=pk)
    
    if request.method == 'POST':
        form = PrixVenteForm(request.POST)
        if form.is_valid():
            prix_vente = form.save(commit=False)
            prix_vente.produit = produit
            
            # Si ce prix est défini comme actif, désactiver les autres
            if prix_vente.actif:
                produit.prix_vente_historique.update(actif=False)
            
            prix_vente.save()
            messages.success(request, 'Нова ціна продажу успішно додана!')
            return redirect('detail_produit', pk=produit.pk)
    else:
        form = PrixVenteForm()
    
    return render(request, 'inventory/form_prix_vente.html', {
        'form': form,
        'produit': produit,
        'title': f'Додати ціну для {produit.description}'
    })


def toggle_prix_actif(request, pk, prix_pk):
    """Activer/désactiver un prix de vente"""
    produit = get_object_or_404(Produit, pk=pk)
    prix = get_object_or_404(PrixVente, pk=prix_pk, produit=produit)
    
    if request.method == 'POST':
        if not prix.actif:
            # Désactiver tous les autres prix
            produit.prix_vente_historique.update(actif=False)
            prix.actif = True
            prix.save()
            messages.success(request, 'Ціна активована!')
        else:
            prix.actif = False
            prix.save()
            messages.success(request, 'Ціна деактивована!')
        
        return redirect('detail_produit', pk=produit.pk)
    
    return redirect('detail_produit', pk=pk)

def get_prix_produit(request, pk):
    """Retourner les prix disponibles pour un produit (AJAX)"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        produit = get_object_or_404(Produit, pk=pk)
        prix_list = []
        
        # Prix de base
        prix_list.append({
            'id': '',
            'prix': float(produit.prix_vente),
            'label': f'Prix de base: {produit.prix_vente}€'
        })
        
        # Prix négociés actifs
        for prix in produit.prix_vente_historique.filter(actif=True):
            label = f'{prix.prix}€'
            if prix.client:
                label += f' ({prix.client})'
            prix_list.append({
                'id': prix.id,
                'prix': float(prix.prix),
                'label': label
            })
        
        return JsonResponse({'prix': prix_list})
    
    return JsonResponse({'error': 'Requête invalide'}, status=400)
