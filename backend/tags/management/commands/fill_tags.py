import csv
import os

from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        tags = os.path.join('data/', 'tags.csv')
        with open(
            tags, encoding='utf-8'
        ) as csvfile:
            csvreader = csv.reader(csvfile)
            counter = 0
            for row in csvreader:
                Tag.objects.create(
                    name=row[0],
                    slug=row[1],
                    color=row[2]
                )
                counter += 1
