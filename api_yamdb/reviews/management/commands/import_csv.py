import os
from csv import DictReader

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from reviews.models import Comments, Category, Genre, GenreTitle, User, Reviews, Title

CSV_PATH = os.path.join(settings.BASE_DIR, 'static/data/')
MODELS = (
    (User, 'users.csv'),
    (Category, 'category.csv'),
    (Genre, 'genre.csv'),
    (Title, 'titles.csv'),
    (Reviews, 'review.csv'),
    (Comments, 'comments.csv'),
    (GenreTitle, 'genre_title.csv'),
)


class Command(BaseCommand):
    help = 'Импорт данных из csv файлов в БД'

    def handle(self, *args, **options):
        for model in MODELS:
            with open(CSV_PATH + model[1], newline='') as csvfile:
                reader = DictReader(csvfile)
                next(reader)
            for row in reader:
                pass
                # что-то типа...
                # model[0].objects.bulk_create()
