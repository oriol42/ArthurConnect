from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

# Create your models here.

class Category(models.Model):
    """Catégorie des produits/formations"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    """Produit/Formation"""
    PRODUCT_TYPES = [
        ('formation', 'Formation'),
        ('article', 'Article'),
        ('service', 'Service'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES, default='formation')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    # Prix et promotion
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_percentage = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Images
    main_image = models.ImageField(upload_to='products/', blank=True, null=True)
    gallery = models.JSONField(default=list, blank=True)  # Liste d'URLs d'images
    
    # Contenu de formation
    video_urls = models.JSONField(default=list, blank=True)  # Liste de vidéos YouTube
    duration_hours = models.PositiveIntegerField(default=0)  # Durée en heures
    level = models.CharField(max_length=20, choices=[
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
    ], default='debutant')
    
    # Stock et disponibilité
    stock_quantity = models.PositiveIntegerField(default=0)
    is_digital = models.BooleanField(default=True)  # Produit numérique
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        """Prix final après réduction"""
        if self.old_price and self.discount_percentage > 0:
            from decimal import Decimal
            discount_factor = Decimal(1) - Decimal(self.discount_percentage) / Decimal(100)
            return self.old_price * discount_factor
        return self.price

    @property
    def is_on_sale(self):
        """Vérifie si le produit est en promotion"""
        return self.old_price and self.discount_percentage > 0

class Cart(models.Model):
    """Panier d'achat"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    session_key = models.CharField(max_length=100, blank=True, null=True)  # Pour les utilisateurs non connectés
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"

    def __str__(self):
        return f"Panier de {self.user.username if self.user else 'Session'}"

    @property
    def total_price(self):
        """Prix total du panier"""
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        """Nombre total d'articles dans le panier"""
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    """Article dans le panier"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Article du panier"
        verbose_name_plural = "Articles du panier"
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def total_price(self):
        """Prix total pour cet article"""
        return self.product.final_price * self.quantity

class Order(models.Model):
    """Commande"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('processing', 'En cours de traitement'),
        ('shipped', 'Expédiée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
        ('refunded', 'Remboursée'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('paid', 'Payée'),
        ('failed', 'Échouée'),
        ('refunded', 'Remboursée'),
    ]

    order_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    
    # Informations de livraison
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Cameroun')
    
    # Statuts
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Prix
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-created_at']

    def __str__(self):
        return f"Commande {self.order_number} - {self.user.username}"

class OrderItem(models.Model):
    """Article de commande"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Prix au moment de la commande
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

class Payment(models.Model):
    """Paiement"""
    PAYMENT_METHODS = [
        ('mtn_money', 'MTN Money'),
        ('orange_money', 'Orange Money'),
        ('mobile_money', 'Mobile Money (Autre)'),
        ('bank_transfer', 'Virement bancaire'),
        ('cash', 'Espèces'),
        ('crypto', 'Cryptomonnaie'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Order.PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"

    def __str__(self):
        return f"Paiement {self.transaction_id} - {self.order.order_number}"

class Review(models.Model):
    """Avis sur les produits"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified = models.BooleanField(default=False)  # Achat vérifié
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"
        unique_together = ['product', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"Avis de {self.user.username} sur {self.product.name}"

class Wishlist(models.Model):
    """Liste de souhaits"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Liste de souhaits"
        verbose_name_plural = "Listes de souhaits"
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class ContactMessage(models.Model):
    """Messages de contact"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-created_at']

    def __str__(self):
        return f"Message de {self.name} - {self.subject}"
