from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Produit(models.Model):
    """Modèle pour les produits"""
    description = models.CharField(max_length=200, verbose_name="Опис")
    cout_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Собівартість (базова)",
        help_text="Базова собівартість товару"
    )
    prix_vente = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Ціна продажу (базова)",
        help_text="Базова ціна продажу"
    )
    photo = models.ImageField(
        upload_to='produits/',
        blank=True,
        null=True,
        verbose_name="Фото товару",
        help_text="Зображення товару"
    )
    seuil_alerte = models.PositiveIntegerField(
        default=10,
        verbose_name="Поріг попередження",
        help_text="Мінімальна кількість для попередження"
    )
    date_creation = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата створення"
    )
    date_modification = models.DateTimeField(
        auto_now=True, verbose_name="Дата зміни"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ['description']

    def __str__(self):
        return self.description

    def stock_actuel(self):
        """Calcule le stock actuel (entrées - sorties)"""
        from django.db.models import Sum
        entrees = self.mouvement_set.filter(
            type_mouvement='entree'
        ).aggregate(total=Sum('quantite'))['total'] or 0
        sorties = self.mouvement_set.filter(
            type_mouvement='sortie'
        ).aggregate(total=Sum('quantite'))['total'] or 0
        return entrees - sorties

    def est_en_rupture(self):
        """Vérifie si le produit est en rupture de stock"""
        return self.stock_actuel() <= 0

    def est_en_alerte(self):
        """Vérifie si le produit est en dessous du seuil d'alerte"""
        return self.stock_actuel() <= self.seuil_alerte

    def statut_stock(self):
        """Retourne le statut du stock (normal, alerte, rupture)"""
        stock = self.stock_actuel()
        if stock <= 0:
            return 'rupture'
        elif stock <= self.seuil_alerte:
            return 'alerte'
        else:
            return 'normal'

    def valeur_stock(self):
        """Calcule la valeur du stock actuel (quantité × coût actuel)"""
        return self.stock_actuel() * self.cout_achat_actuel()

    def prix_vente_actuel(self):
        """Retourne le prix de vente le plus récent ou le prix de base"""
        dernier_prix = self.prix_vente_historique.filter(actif=True).order_by('-date_creation').first()
        return dernier_prix.prix if dernier_prix else self.prix_vente

    def cout_achat_actuel(self):
        """Retourne le coût d'achat le plus récent ou le coût de base"""
        dernier_cout = self.cout_achat_historique.filter(
            actif=True
        ).order_by('-date_creation').first()
        return dernier_cout.cout if dernier_cout else self.cout_achat

    def marge_beneficiaire(self):
        """Calcule la marge bénéficiaire actuelle"""
        return self.prix_vente_actuel() - self.cout_achat_actuel()


class CoutAchat(models.Model):
    """Modèle pour l'historique des coûts d'achat variables"""
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='cout_achat_historique',
        verbose_name="Товар"
    )
    cout = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Собівартість"
    )
    fournisseur = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Постачальник",
        help_text="Постачальник або контекст для цієї вартості"
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Активна",
        help_text="Чи активна ця вартість для використання"
    )
    commentaire = models.TextField(
        blank=True,
        verbose_name="Коментар",
        help_text="Причина зміни вартості або деталі закупівлі"
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення"
    )

    class Meta:
        verbose_name = "Собівартість"
        verbose_name_plural = "Собівартості"
        ordering = ['-date_creation']

    def __str__(self):
        fournisseur_info = f" ({self.fournisseur})" if self.fournisseur else ""
        return f"{self.produit.description} - {self.cout}€{fournisseur_info}"


class PrixVente(models.Model):
    """Modèle pour l'historique des prix de vente négociés"""
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='prix_vente_historique',
        verbose_name="Товар"
    )
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Ціна продажу"
    )
    client = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Клієнт",
        help_text="Клієнт або контекст для цієї ціни"
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Активна",
        help_text="Чи активна ця ціна для використання"
    )
    commentaire = models.TextField(
        blank=True,
        verbose_name="Коментар",
        help_text="Причина зміни ціни або деталі переговорів"
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення"
    )

    class Meta:
        verbose_name = "Ціна продажу"
        verbose_name_plural = "Ціни продажу"
        ordering = ['-date_creation']

    def __str__(self):
        client_info = f" ({self.client})" if self.client else ""
        return f"{self.produit.description} - {self.prix}€{client_info}"


class Mouvement(models.Model):
    """Modèle pour les mouvements de stock"""
    TYPE_CHOICES = [
        ('entree', 'Надходження'),
        ('sortie', 'Вихід'),
    ]

    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    type_mouvement = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name="Тип операції"
    )
    quantite = models.PositiveIntegerField(verbose_name="Кількість")
    prix_vente_utilise = models.ForeignKey(
        PrixVente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ціна продажу використана",
        help_text="Ціна продажу використана для цієї операції "
                  "(тільки для виходів)"
    )
    cout_achat_utilise = models.ForeignKey(
        'CoutAchat',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Собівартість використана",
        help_text="Собівартість використана для цієї операції "
                  "(тільки для надходжень)"
    )
    date_mouvement = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата операції"
    )
    commentaire = models.TextField(blank=True, verbose_name="Коментар")

    class Meta:
        verbose_name = "Рух товару"
        verbose_name_plural = "Рухи товарів"
        ordering = ['-date_mouvement']

    def __str__(self):
        return (f"{self.get_type_mouvement_display()} - "
                f"{self.produit.description} ({self.quantite})")

    def prix_utilise(self):
        """Retourne le prix utilisé pour ce mouvement"""
        if self.type_mouvement == 'sortie' and self.prix_vente_utilise:
            return self.prix_vente_utilise.prix
        elif self.type_mouvement == 'sortie':
            return self.produit.prix_vente_actuel()
        return None

    def cout_utilise(self):
        """Retourne le coût d'achat utilisé pour ce mouvement"""
        if self.type_mouvement == 'entree' and self.cout_achat_utilise:
            return self.cout_achat_utilise.cout
        elif self.type_mouvement == 'entree':
            return self.produit.cout_achat_actuel()
        return None

    def valeur_mouvement(self):
        """Calcule la valeur du mouvement"""
        if self.type_mouvement == 'sortie':
            prix = self.prix_utilise()
            return self.quantite * prix if prix else 0
        elif self.type_mouvement == 'entree':
            cout = self.cout_utilise()
            return self.quantite * cout if cout else 0
        return 0
