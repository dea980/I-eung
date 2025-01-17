import csv
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from articles.models import Recipe, Category

class Command(BaseCommand):
    help = 'Load recipes from CSV file'

    def handle(self, *args, **kwargs):
        # Create a default user if not exists
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )

        # Create default category
        category, created = Category.objects.get_or_create(
            name='한식',
            defaults={'description': '한국 전통 요리'}
        )

        # Get the absolute path to the CSV file
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), 'RECIPE_DATA.csv')
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                try:
                    serving_size = int(row['CKG_INBUN_NM'].replace('인분', '')) if row['CKG_INBUN_NM'] and '인분' in row['CKG_INBUN_NM'] else 2
                except (ValueError, AttributeError):
                    serving_size = 2

                recipe = Recipe.objects.create(
                    name=row['RCP_TTL'],
                    author=user,
                    description=row['CKG_IPDC'],
                    cooking_time=30,  # Default value
                    difficulty='easy',
                    serving_size=serving_size
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created recipe: {recipe.name}'))