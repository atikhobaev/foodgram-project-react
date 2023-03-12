import csv
import os
import random

from django.core.management.base import BaseCommand

from recipes.models import Recipe

from users.models import User

users = User.objects.all().exclude(is_superuser=True)


# рецепты сформировала через чат нейронка you.com
class Command(BaseCommand):
    def handle(self, *args, **options):
        recipes = os.path.join('data/', 'recipes.csv')
        with open(
            recipes, encoding='utf-8'
        ) as csvfile:
            csvreader = csv.reader(csvfile)
            counter = 0
            for row in csvreader:
                user = random.choice(users)
                Recipe.objects.create(
                    author=user,
                    name=row[0],
                    cooking_time=row[1],
                    text=row[2]
                )
                counter += 1
