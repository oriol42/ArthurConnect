from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Product, Cart, CartItem, Order, OrderItem, 
    Payment, Review, Wishlist, ContactMessage
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'product_type', 'price', 'is_active', 'is_featured', 'created_at']
    list_filter = ['product_type', 'category', 'is_active', 'is_featured', 'level', 'created_at']
    search_fields = ['name', 'description', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = []
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'slug', 'description', 'short_description', 'product_type', 'category')
        }),
        ('Prix et promotion', {
            'fields': ('price', 'old_price', 'discount_percentage')
        }),
        ('Images', {
            'fields': ('main_image', 'gallery')
        }),
        ('Contenu de formation', {
            'fields': ('video_urls', 'duration_hours', 'level')
        }),
        ('Stock et disponibilité', {
            'fields': ('stock_quantity', 'is_digital', 'is_active', 'is_featured')
        }),
        ('Métadonnées', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['added_at']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'payment_status', 'total_amount', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at', 'country']
    search_fields = ['order_number', 'user__username', 'email', 'first_name', 'last_name']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Informations de commande', {
            'fields': ('order_number', 'user', 'status', 'payment_status')
        }),
        ('Informations de livraison', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'postal_code', 'country')
        }),
        ('Prix', {
            'fields': ('subtotal', 'tax_amount', 'shipping_cost', 'total_amount')
        }),
        ('Métadonnées', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'order', 'payment_method', 'amount', 'status', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['transaction_id', 'order__order_number']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_verified', 'created_at']
    list_filter = ['rating', 'is_verified', 'created_at']
    search_fields = ['product__name', 'user__username', 'title']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['added_at']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
