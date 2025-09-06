from django.urls import path
from . import views

urlpatterns = [
    # Pages principales
    path('', views.index, name='index'),
    path('home/', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('service-client/', views.service_client, name='service_client'),
    
    # Boutique
    path('boutique/formations/', views.boutique_formations, name='boutique_formations'),
    path('boutique/articles/', views.boutique_articles, name='boutique_articles'),
    
    # Produits/Formations (ancien)
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Authentification
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    
    # Panier et commandes
    path('cart/', views.cart_view, name='cart'),
    path('cart-count/', views.cart_count, name='cart_count'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('my-orders/', views.my_orders, name='my_orders'),
    
    # Favoris
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    
    # Avis
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
]