import os
from csv import DictReader

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.management.commands._orm_func_for_import import (
    category_create, comment_create, genre_create, genre_title_create,
    review_create, title_create, user_create)

SUCCESS_IMPORT = 'Импорт файла {} завершен успешно!'
CSV_PATH = os.path.join(settings.BASE_DIR, 'static/data/')
FILE_AND_MODEL = {
    'category.csv': category_create,
    'genre.csv': genre_create,
    'titles.csv': title_create,
    'genre_title.csv': genre_title_create,
    'users.csv': user_create,
    'review.csv': review_create,
    'comments.csv': comment_create,
}


class Command(BaseCommand):
    help = 'Импорт данных из csv файлов в БД'

    def handle(self, *args, **options):
        for filename, model in FILE_AND_MODEL.items():
            with open(CSV_PATH + filename, 'r', encoding='utf-8') as csvfile:
                reader = DictReader(csvfile)
                next(reader)
                for row in reader:
                    model(row)
            self.stdout.write(
                self.style.SUCCESS(SUCCESS_IMPORT.format(filename)))
