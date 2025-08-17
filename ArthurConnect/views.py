from django.shortcuts import render

def index(request):
  return render(request,'ArthurConnect/index.html')

def article(request):
    return render(request,'ArthurConnect/article.html')

def contact(request):
  return render(request,'ArthurConnect/contact.html')

def cart(request):
  return render(request,'ArthurConnect/cart.html')

def checkout(request):
  return render(request,'ArthurConnect/checkout.html')

def about(request):
  return render(request,'ArthurConnect/about.html')

def service_client(request):
  return render(request,'ArthurConnect/service-client.html')

def formation(request):
    return render(request,'ArthurConnect/formation.html')

def formation_detail(request, formation_id):
    # Pour l'instant, données fictives, à remplacer par une vraie requête DB plus tard
    formations = [
        {
            'id': 1,
            'titre': 'Python pour débutants',
            'description': "Apprenez les bases du Python en vidéo, accessible à tous, même si vous n'avez jamais programmé auparavant. Cette formation couvre les fondamentaux, les structures de données, et bien plus encore pour vous lancer rapidement.",
            'categorie': 'Alibaba',
            'prix': '29,99 €',
            'ancien_prix': '49,99 €',
            'image': 'ArthurConnect/img/banner/banner-bg.jpg',
            'videos': [
                {'titre': 'Introduction', 'url': 'https://www.youtube.com/embed/_uQrJ0TkZlc'},
                {'titre': 'Variables et Types', 'url': 'https://www.youtube.com/embed/kqtD5dpn9C8'},
            ]
        },
        {
            'id': 2,
            'titre': 'Développement Web Moderne',
            'description': "Créez des sites web dynamiques avec les dernières technologies front-end et back-end. Cette formation vous guide de A à Z, même sans prérequis technique.",
            'categorie': 'Pinduoduo',
            'prix': '39,99 €',
            'ancien_prix': None,
            'image': 'ArthurConnect/img/banner/homephoto1.jpg',
            'videos': [
                {'titre': 'HTML & CSS', 'url': 'https://www.youtube.com/embed/UB1O30fR-EE'},
                {'titre': 'JS & Backend', 'url': 'https://www.youtube.com/embed/3PHXvlpOkf4'},
            ]
        },
        {
            'id': 3,
            'titre': 'Achat malin au Nigeria',
            'description': "Découvrez comment acheter efficacement au Nigeria, astuces, plateformes fiables et conseils pour réussir vos achats à distance.",
            'categorie': 'Achat au Nigeria',
            'prix': '24,99 €',
            'ancien_prix': None,
            'image': 'ArthurConnect/img/banner/homephoto3.jpg',
            'videos': [
                {'titre': 'Introduction à l’achat', 'url': 'https://www.youtube.com/embed/2VJlzeEVL8A'},
            ]
        },
        {
            'id': 4,
            'titre': 'Publicité Facebook efficace',
            'description': "Maîtrisez la publicité Facebook pour booster votre business, générer des ventes et toucher la bonne audience.",
            'categorie': 'Publicité Facebook',
            'prix': '34,99 €',
            'ancien_prix': None,
            'image': 'ArthurConnect/img/banner/banner-bg.jpg',
            'videos': [
                {'titre': 'Créer une campagne', 'url': 'https://www.youtube.com/embed/eM3q-BjGkAU'},
            ]
        },
    ]
    formation = next((f for f in formations if f['id'] == formation_id), None)
    if not formation:
        from django.http import Http404
        raise Http404('Formation non trouvée')
    return render(request, 'ArthurConnect/formation_detail.html', {'formation': formation})

def article_detail(request, article_id):
    # Données fictives pour l'exemple
    articles = [
        {
            'id': 1,
            'titre': "Sneaker Homme Moderne",
            'description': "Une sneaker tendance pour homme, confortable et stylée.",
            'categorie': "Chaussures",
            'prix': "25,00 €",
            'ancien_prix': "35,00 €",
            'image': 'ArthurConnect/img/product/inspired-product/i1.jpg',
        },
        {
            'id': 2,
            'titre': "Montre Élégante",
            'description': "Montre élégante pour toutes les occasions.",
            'categorie': "Accessoires",
            'prix': "49,00 €",
            'ancien_prix': None,
            'image': 'ArthurConnect/img/product/inspired-product/i2.jpg',
        },
        # ... autres articles ...
    ]
    article = next((a for a in articles if a['id'] == article_id), None)
    if not article:
        from django.http import Http404
        raise Http404('Article non trouvé')
    return render(request, 'ArthurConnect/article_detail.html', {'article': article})