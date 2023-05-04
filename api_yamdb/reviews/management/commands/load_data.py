import csv

from django.conf import settings
from django.core.management import BaseCommand

from ...models import Category, Comment, Genre, Review, Title

MODELS = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    settings.AUTH_USER_MODEL: 'users.csv',
}


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for model, file in MODELS.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{file}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(
                    model(**data) for data in reader)
