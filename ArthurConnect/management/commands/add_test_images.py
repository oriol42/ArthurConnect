from django.core.management.base import BaseCommand
from ArthurConnect.models import Product
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Ajoute des images de test aux produits'

    def handle(self, *args, **options):
        # Copier des images existantes comme images de test
        source_images = {
            'formation': 'ArthurConnect/static/ArthurConnect/img/banner/banner-bg.jpg',
            'chaussures': 'ArthurConnect/static/ArthurConnect/img/banner/homephoto.JPG',
            'vetements': 'ArthurConnect/static/ArthurConnect/img/banner/homephoto1.jpg',
            'accessoires': 'ArthurConnect/static/ArthurConnect/img/banner/homephoto3.jpg',
        }
        
        for product in Product.objects.all():
            if not product.main_image:
                # Déterminer le type d'image selon la catégorie
                if product.product_type == 'formation':
                    image_path = source_images['formation']
                elif 'chaussures' in product.category.slug:
                    image_path = source_images['chaussures']
                elif 'vetements' in product.category.slug:
                    image_path = source_images['vetements']
                else:
                    image_path = source_images['accessoires']
                
                # Copier l'image vers le répertoire media
                source_path = os.path.join(settings.BASE_DIR, image_path)
                if os.path.exists(source_path):
                    # Créer un nom de fichier unique
                    filename = f"{product.slug}.jpg"
                    dest_path = os.path.join(settings.MEDIA_ROOT, 'products', filename)
                    
                    # Copier le fichier
                    import shutil
                    shutil.copy2(source_path, dest_path)
                    
                    # Mettre à jour le produit
                    product.main_image = f'products/{filename}'
                    product.save()
                    
                    self.stdout.write(f'Image ajoutée pour: {product.name}')
                else:
                    self.stdout.write(f'Image source non trouvée: {source_path}')
        
        self.stdout.write('Images de test ajoutées avec succès!')
