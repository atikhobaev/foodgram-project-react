import csv
import os

from django.core.management.base import BaseCommand

from users.models import User

# генерирую через randomuser.me
# https://randomuser.me/api/?format=csv&inc=login,email,name&nat=us&password=special,upper,lower,number,8-16&results=10


class Command(BaseCommand):
    def handle(self, *args, **options):
        users_csv = os.path.join('data/', 'users.csv')
        with open(
            users_csv, encoding='utf-8'
        ) as csvfile:
            csvreader = csv.reader(csvfile)
            counter = 0
            for row in csvreader:
                if row[0] == 'name.title':
                    continue
                User.objects.get_or_create(
                        username=row[5],
                        password=row[6],
                        email=row[3],
                        first_name=row[1],
                        last_name=row[2]
                    )
                user = User.objects.get(username=row[5])
                user.set_password(user.password)
                user.save()
                counter += 1
