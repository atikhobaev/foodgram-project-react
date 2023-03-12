import csv
import os

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        ingredients = os.path.join('data/', 'ingredients.csv')
        with open(
            ingredients, encoding='utf-8'
        ) as csvfile:
            csvreader = csv.reader(csvfile)
            counter = 0
            for row in csvreader:
                Ingredient.objects.create(name=row[0], measurement_unit=row[1])
                counter += 1
