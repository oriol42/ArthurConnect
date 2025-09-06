from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ArthurConnect.models import Category, Product

class Command(BaseCommand):
    help = 'Peuple la base de données avec des données de test'

    def handle(self, *args, **options):
        # Créer des catégories
        categories_data = [
            # Formations
            {
                'name': 'Achat en Chine',
                'slug': 'achat-chine',
                'description': 'Formations sur l\'achat et l\'import depuis la Chine'
            },
            {
                'name': 'Achat au Nigeria',
                'slug': 'achat-nigeria',
                'description': 'Formations sur le commerce et l\'achat au Nigeria'
            },
            {
                'name': 'Publicité Facebook',
                'slug': 'publicite-facebook',
                'description': 'Formations en publicité Facebook et marketing digital'
            },
            {
                'name': 'E-commerce',
                'slug': 'e-commerce',
                'description': 'Formations en e-commerce et vente en ligne'
            },
            # Articles physiques
            {
                'name': 'Chaussures',
                'slug': 'chaussures',
                'description': 'Chaussures pour homme et femme'
            },
            {
                'name': 'Vêtements',
                'slug': 'vetements',
                'description': 'Vêtements tendance pour tous'
            },
            {
                'name': 'Accessoires',
                'slug': 'accessoires',
                'description': 'Accessoires de mode et lifestyle'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'Catégorie créée: {category.name}')

        # Créer des produits/formations
        products_data = [
            # Formations
            {
                'name': 'Achat en Chine - Guide Complet',
                'slug': 'achat-chine-guide-complet',
                'description': "Apprenez à acheter efficacement en Chine, découvrir les meilleures plateformes (Alibaba, 1688, Taobao), négocier avec les fournisseurs, gérer les frais de port et l'importation. Formation complète pour débuter dans l'import depuis la Chine.",
                'short_description': 'Formation complète sur l\'achat en Chine',
                'product_type': 'formation',
                'category_slug': 'achat-chine',
                'price': 49.99,
                'old_price': 79.99,
                'discount_percentage': 38,
                'duration_hours': 12,
                'level': 'debutant',
                'is_featured': True,
                'video_urls': [
                    {'titre': 'Introduction à l\'achat en Chine', 'url': 'https://www.youtube.com/embed/_uQrJ0TkZlc'},
                    {'titre': 'Plateformes chinoises', 'url': 'https://www.youtube.com/embed/kqtD5dpn9C8'},
                ]
            },
            {
                'name': 'Commerce au Nigeria - Stratégies Gagnantes',
                'slug': 'commerce-nigeria-strategies',
                'description': "Découvrez les opportunités commerciales au Nigeria, les meilleures pratiques pour vendre, les plateformes locales, la gestion des paiements et les défis à surmonter. Formation pratique pour réussir au Nigeria.",
                'short_description': 'Formation sur le commerce au Nigeria',
                'product_type': 'formation',
                'category_slug': 'achat-nigeria',
                'price': 39.99,
                'old_price': 59.99,
                'discount_percentage': 33,
                'duration_hours': 10,
                'level': 'debutant',
                'is_featured': True,
                'video_urls': [
                    {'titre': 'Introduction au marché nigérian', 'url': 'https://www.youtube.com/embed/2VJlzeEVL8A'},
                ]
            },
            {
                'name': 'Publicité Facebook - De A à Z',
                'slug': 'publicite-facebook-complete',
                'description': "Maîtrisez la publicité Facebook et Instagram pour booster votre business. Apprenez à créer des campagnes efficaces, cibler la bonne audience, optimiser vos budgets et analyser vos résultats.",
                'short_description': 'Formation complète publicité Facebook',
                'product_type': 'formation',
                'category_slug': 'publicite-facebook',
                'price': 59.99,
                'old_price': 89.99,
                'discount_percentage': 33,
                'duration_hours': 15,
                'level': 'debutant',
                'is_featured': True,
                'video_urls': [
                    {'titre': 'Créer une campagne Facebook', 'url': 'https://www.youtube.com/embed/eM3q-BjGkAU'},
                ]
            },
            # Articles physiques - Chaussures
            {
                'name': 'Sneakers Homme Moderne',
                'slug': 'sneakers-homme-moderne',
                'description': "Sneakers tendance pour homme, confortables et stylées. Parfaites pour le quotidien et les sorties. Matériaux de qualité et design moderne.",
                'short_description': 'Sneakers confortables et stylées',
                'product_type': 'article',
                'category_slug': 'chaussures',
                'price': 25.00,
                'old_price': 35.00,
                'discount_percentage': 29,
                'duration_hours': 0,
                'level': 'debutant',
                'is_featured': True,
                'is_digital': False,
                'stock_quantity': 50,
                'video_urls': []
            },
            {
                'name': 'Baskets Femme Élégantes',
                'slug': 'baskets-femme-elegantes',
                'description': "Baskets élégantes pour femme, parfaites pour toutes les occasions. Design raffiné et confort optimal. Disponibles en plusieurs couleurs.",
                'short_description': 'Baskets élégantes pour femme',
                'product_type': 'article',
                'category_slug': 'chaussures',
                'price': 29.99,
                'old_price': 39.99,
                'discount_percentage': 25,
                'duration_hours': 0,
                'level': 'debutant',
                'is_featured': False,
                'is_digital': False,
                'stock_quantity': 30,
                'video_urls': []
            },
            # Articles physiques - Vêtements
            {
                'name': 'T-shirt Premium Homme',
                'slug': 't-shirt-premium-homme',
                'description': "T-shirt premium pour homme en coton de qualité supérieure. Coupe moderne et confortable. Disponible en plusieurs couleurs et tailles.",
                'short_description': 'T-shirt premium en coton',
                'product_type': 'article',
                'category_slug': 'vetements',
                'price': 15.99,
                'old_price': 22.99,
                'discount_percentage': 30,
                'duration_hours': 0,
                'level': 'debutant',
                'is_featured': True,
                'is_digital': False,
                'stock_quantity': 100,
                'video_urls': []
            },
            {
                'name': 'Robe Femme Chic',
                'slug': 'robe-femme-chic',
                'description': "Robe chic et élégante pour femme, parfaite pour les occasions spéciales. Coupe flatteuse et tissu de qualité. Disponible en plusieurs tailles.",
                'short_description': 'Robe chic et élégante',
                'product_type': 'article',
                'category_slug': 'vetements',
                'price': 39.99,
                'old_price': 54.99,
                'discount_percentage': 27,
                'duration_hours': 0,
                'level': 'debutant',
                'is_featured': False,
                'is_digital': False,
                'stock_quantity': 25,
                'video_urls': []
            },
            # Articles physiques - Accessoires
            {
                'name': 'Montre Élégante Homme',
                'slug': 'montre-elegante-homme',
                'description': "Montre élégante pour homme, parfaite pour toutes les occasions. Design classique et moderne. Mouvement précis et bracelet en cuir de qualité.",
                'short_description': 'Montre élégante pour homme',
                'product_type': 'article',
                'category_slug': 'accessoires',
                'price': 49.99,
                'old_price': 69.99,
                'discount_percentage': 29,
                'duration_hours': 0,
                'level': 'debutant',
                'is_featured': True,
                'is_digital': False,
                'stock_quantity': 20,
                'video_urls': []
            },
            {
                'name': 'Sac à Main Tendance',
                'slug': 'sac-main-tendance',
                'description': "Sac à main tendance pour femme, spacieux et élégant. Parfait pour le quotidien et les sorties. Matériaux de qualité et design moderne.",
                'short_description': 'Sac à main tendance',
                'product_type': 'article',
                'category_slug': 'accessoires',
                'price': 34.99,
                'old_price': 49.99,
                'discount_percentage': 30,
                'duration_hours': 0,
                'level': 'debutant',
                'is_featured': False,
                'is_digital': False,
                'stock_quantity': 40,
                'video_urls': []
            }
        ]

        # Obtenir l'utilisateur admin
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@arthurconnect.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )

        for product_data in products_data:
            category = categories[product_data['category_slug']]
            del product_data['category_slug']
            
            # Valeurs par défaut
            defaults = {
                'category': category,
                'created_by': admin_user,
                'is_active': True,
            }
            
            # Ajouter les champs spécifiques selon le type de produit
            if product_data.get('is_digital') is not None:
                defaults['is_digital'] = product_data['is_digital']
            else:
                defaults['is_digital'] = product_data['product_type'] == 'formation'
            
            if product_data.get('stock_quantity') is not None:
                defaults['stock_quantity'] = product_data['stock_quantity']
            else:
                defaults['stock_quantity'] = 100 if product_data['product_type'] == 'formation' else 50
            
            # Supprimer les champs qui ne sont pas dans le modèle
            product_data_clean = {k: v for k, v in product_data.items() if k not in ['category_slug', 'is_digital', 'stock_quantity']}
            
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults={**product_data_clean, **defaults}
            )
            
            if created:
                self.stdout.write(f'Produit créé: {product.name}')
            else:
                self.stdout.write(f'Produit existant: {product.name}')

        self.stdout.write(
            self.style.SUCCESS('Données de test créées avec succès!')
        )
