from django import forms
from .models import Produit, Mouvement, PrixVente


class ProduitForm(forms.ModelForm):
    """Formulaire pour les produits"""
    
    class Meta:
        model = Produit
        fields = ['description', 'cout_achat', 'prix_vente', 'seuil_alerte']
        widgets = {
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Опис товару'}
            ),
            'cout_achat': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}
            ),
            'prix_vente': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}
            ),
            'seuil_alerte': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '0'}
            ),
        }


class PrixVenteForm(forms.ModelForm):
    """Formulaire pour ajouter un nouveau prix de vente négocié"""
    
    class Meta:
        model = PrixVente
        fields = ['prix', 'client', 'commentaire', 'actif']
        widgets = {
            'prix': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}
            ),
            'client': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Назва клієнта або контекст (необов\'язково)'
                }
            ),
            'commentaire': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Причина зміни ціни або деталі переговорів'
                }
            ),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MouvementForm(forms.ModelForm):
    """Formulaire pour les mouvements"""
    
    class Meta:
        model = Mouvement
        fields = ['produit', 'type_mouvement', 'quantite', 'commentaire']
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-select'}),
            'type_mouvement': forms.Select(attrs={'class': 'form-select'}),
            'quantite': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '1'}
            ),
            'commentaire': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Коментар (необов\'язково)'
                }
            ),
        }


class FiltreMovementForm(forms.Form):
    """Formulaire de filtrage des mouvements"""
    TYPE_CHOICES = [
        ('', 'Всі типи'),
        ('entree', 'Надходження'),
        ('sortie', 'Вихід'),
    ]
    
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}
        ),
        label='Дата початку'
    )
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}
        ),
        label='Дата кінця'
    )
    type_mouvement = forms.ChoiceField(
        choices=TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Тип операції'
    )
    produit = forms.ModelChoiceField(
        queryset=Produit.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Товар',
        empty_label='Всі товари'
    )
