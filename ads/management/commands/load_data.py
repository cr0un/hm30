import os
import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from ads.models import Category, Ad
from users.models import User, Location

BASE_DIR = settings.BASE_DIR
DATASETS_DIR = os.path.join(BASE_DIR, 'datasets')


class Command(BaseCommand):
    help = 'Загрузка данных из CSV файлов в таблицы БД postgres'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Загрузка categories
            with open(os.path.join(DATASETS_DIR, 'category.csv'), newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Category.objects.create(
                        # id=row['id'],
                        name=row['name']
                    )
            self.stdout.write(self.style.SUCCESS('Успешно загружен categories'))


            # Загрузка locations
            with open(os.path.join(DATASETS_DIR, 'location.csv'), newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Location.objects.create(
                        # id=row['id'],
                        name=row['name'],
                        lat=row['lat'],
                        lng=row['lng']
                    )
            self.stdout.write(self.style.SUCCESS('Успешно загружен locations'))


            # Загрузка users
            with open(os.path.join(DATASETS_DIR, 'user.csv'), newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    user_id = row.get('id', None)
                    if user_id:
                        user_id = int(user_id)
                    user = User.objects.create(
                        # id=user_id,
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        username=row['username'],
                        password=row['password'],
                        role=row['role'],
                        age=row['age'],
                    )
                    location_id = row.get('location_id', None)
                    if location_id:
                        try:
                            location = Location.objects.get(id=location_id)
                            user.locations.add(location)  # добавление связи между User и Location
                            self.stdout.write(self.style.SUCCESS(
                                f"Добавлена связь между пользователем {user.username} и локацией {location.name}"))
                        except Location.DoesNotExist:
                            pass

            self.stdout.write(self.style.SUCCESS('Успешно загружен users'))


            # Загрузка ads
            with open(os.path.join(DATASETS_DIR, 'ad.csv'), newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    is_published = True if row['is_published'].upper() == 'TRUE' else False
                    try:
                        author = User.objects.get(id=row['author_id'])
                        category = Category.objects.get(id=row['category_id'])
                        Ad.objects.create(
                            # id=row['id'],
                            name=row['name'],
                            author=author,
                            price=row['price'],
                            description=row['description'],
                            is_published=is_published,
                            image=row['image'],
                            category=category
                        )
                    except User.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(f"Пользователь с ID {row['author_id']} не найден. Объявление не создано."))
                    except Category.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(f"Категория с ID {row['category_id']} не найдена. Объявление не создано."))

