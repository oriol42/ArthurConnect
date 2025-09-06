from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Product, Category, Cart, CartItem, Order, OrderItem, Payment, Review, Wishlist, ContactMessage
from .forms import UserRegistrationForm, UserLoginForm, ContactForm, ReviewForm, SearchForm

def index(request):
    """Page d'accueil avec les formations vedettes"""
    # Seulement les formations vedettes
    featured_products = Product.objects.filter(is_featured=True, is_active=True, product_type='formation')[:6]
    # Seulement les catégories de formations
    categories = Category.objects.filter(is_active=True, slug__in=['achat-chine', 'achat-nigeria', 'publicite-facebook', 'e-commerce'])
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'ArthurConnect/index.html', context)

def boutique_formations(request):
    """Page boutique - formations uniquement"""
    products = Product.objects.filter(is_active=True, product_type='formation')
    search_form = SearchForm(request.GET)
    
    # Filtres
    if request.GET.get('search'):
        products = products.filter(name__icontains=request.GET['search'])
    
    if request.GET.get('category'):
        products = products.filter(category_id=request.GET['category'])
    
    if request.GET.get('level'):
        products = products.filter(level=request.GET['level'])
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True, slug__in=['achat-chine', 'achat-nigeria', 'publicite-facebook', 'e-commerce'])
    
    context = {
        'products': products,
        'categories': categories,
        'search_form': search_form,
        'product_type': 'formation',
    }
    return render(request, 'ArthurConnect/boutique_formations.html', context)

def boutique_articles(request):
    """Page boutique - articles uniquement"""
    products = Product.objects.filter(is_active=True, product_type='article')
    search_form = SearchForm(request.GET)
    
    # Filtres
    if request.GET.get('search'):
        products = products.filter(name__icontains=request.GET['search'])
    
    if request.GET.get('category'):
        products = products.filter(category_id=request.GET['category'])
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True, slug__in=['chaussures', 'vetements', 'accessoires'])
    
    context = {
        'products': products,
        'categories': categories,
        'search_form': search_form,
        'product_type': 'article',
    }
    return render(request, 'ArthurConnect/boutique_articles.html', context)

def product_list(request):
    """Liste des produits/formations avec filtres (ancienne vue)"""
    products = Product.objects.filter(is_active=True)
    search_form = SearchForm(request.GET)
    
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        category = search_form.cleaned_data.get('category')
        price_min = search_form.cleaned_data.get('price_min')
        price_max = search_form.cleaned_data.get('price_max')
        
        if query:
            products = products.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(short_description__icontains=query)
            )
        
        if category:
            products = products.filter(category=category)
        
        if price_min:
            products = products.filter(price__gte=price_min)
        
        if price_max:
            products = products.filter(price__lte=price_max)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'search_form': search_form,
        'categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'ArthurConnect/product_list.html', context)

def product_detail(request, product_id):
    """Détail d'un produit/formation"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    reviews = Review.objects.filter(product=product, is_verified=True)[:10]
    
    # Formulaire d'avis (si utilisateur connecté et a acheté le produit)
    review_form = None
    if request.user.is_authenticated:
        has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__payment__status='paid'
        ).exists()
        
        if has_purchased and not Review.objects.filter(user=request.user, product=product).exists():
            review_form = ReviewForm()
    
    # Vérifier si l'utilisateur a acheté ce produit
    user_has_purchased = False
    if request.user.is_authenticated:
        user_has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__payment__status='paid'
        ).exists()
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'review_form': review_form,
        'user_has_purchased': user_has_purchased,
    }
    return render(request, 'ArthurConnect/product_detail.html', context)

def contact(request):
    """Page de contact"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre message a été envoyé avec succès!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'ArthurConnect/contact.html', {'form': form})

def about(request):
    """Page à propos"""
    return render(request, 'ArthurConnect/about.html')

def service_client(request):
    """Page service client"""
    return render(request, 'ArthurConnect/service-client.html')

# Authentification
def register(request):
    """Inscription utilisateur"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte créé avec succès!')
            return redirect('index')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'ArthurConnect/auth/register.html', {'form': form})

def user_login(request):
    """Connexion utilisateur"""
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenue {user.first_name}!')
            return redirect('index')
    else:
        form = UserLoginForm()
    
    return render(request, 'ArthurConnect/auth/login.html', {'form': form})

def user_logout(request):
    """Déconnexion utilisateur"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('index')

# Gestion du panier
@login_required
def cart_view(request):
    """Vue du panier"""
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'ArthurConnect/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    """Ajouter un produit au panier"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name} ajouté au panier!')
    return redirect('product_detail', product_id=product_id)

@login_required
def remove_from_cart(request, cart_item_id):
    """Retirer un produit du panier"""
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Produit retiré du panier!')
    return redirect('cart')

@login_required
def update_cart_item(request, cart_item_id):
    """Mettre à jour la quantité d'un article dans le panier"""
    if request.method == 'POST':
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        cart_item.quantity = max(1, quantity)
        cart_item.save()
        
        return JsonResponse({
            'success': True,
            'total_price': float(cart_item.total_price),
            'cart_total': float(cart_item.cart.total_price)
        })
    
    return JsonResponse({'success': False})

@login_required
def checkout(request):
    """Page de commande"""
    cart = get_object_or_404(Cart, user=request.user, is_active=True)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.warning(request, 'Votre panier est vide!')
        return redirect('cart')
    
    if request.method == 'POST':
        # Créer la commande
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            postal_code=request.POST.get('postal_code'),
            country=request.POST.get('country', 'Cameroun'),
            subtotal=cart.total_price,
            total_amount=cart.total_price,
        )
        
        # Créer les articles de commande
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.final_price,
                total_price=cart_item.total_price
            )
        
        # Créer le paiement
        payment = Payment.objects.create(
            order=order,
            payment_method=request.POST.get('payment_method'),
            amount=order.total_amount
        )
        
        # Désactiver le panier
        cart.is_active = False
        cart.save()
        
        messages.success(request, 'Commande créée avec succès!')
        return redirect('order_detail', order_id=order.id)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'ArthurConnect/checkout.html', context)

@login_required
def order_detail(request, order_id):
    """Détail d'une commande"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'ArthurConnect/order_detail.html', {'order': order})

@login_required
def my_orders(request):
    """Mes commandes"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ArthurConnect/my_orders.html', {'orders': orders})

# Favoris
@login_required
def add_to_wishlist(request, product_id):
    """Ajouter aux favoris"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if created:
        messages.success(request, f'{product.name} ajouté aux favoris!')
    else:
        messages.info(request, f'{product.name} est déjà dans vos favoris!')
    
    return redirect('product_detail', product_id=product_id)

@login_required
def remove_from_wishlist(request, product_id):
    """Retirer des favoris"""
    wishlist_item = get_object_or_404(Wishlist, user=request.user, product_id=product_id)
    product_name = wishlist_item.product.name
    wishlist_item.delete()
    messages.success(request, f'{product_name} retiré des favoris!')
    return redirect('wishlist')

@login_required
def wishlist(request):
    """Liste des favoris"""
    wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-added_at')
    return render(request, 'ArthurConnect/wishlist.html', {'wishlist_items': wishlist_items})

# Avis
@login_required
def add_review(request, product_id):
    """Ajouter un avis"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.is_verified = OrderItem.objects.filter(
                order__user=request.user,
                product=product,
                order__payment__status='paid'
            ).exists()
            review.save()
            messages.success(request, 'Votre avis a été publié!')
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm()
    
    return render(request, 'ArthurConnect/add_review.html', {'form': form, 'product': product})

@login_required
def cart_count(request):
    """API pour obtenir le nombre d'articles dans le panier"""
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        count = cart.total_items
    except Cart.DoesNotExist:
        count = 0
    
    return JsonResponse({'count': count})