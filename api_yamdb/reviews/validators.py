import re
import datetime as dt

from rest_framework import serializers
from django.core.exceptions import ValidationError

ERROR_YEAR_FROM_FUTURE = 'Вы ввели {} год, но год выпуска не может быть больше текущего ({})!'


def validate_year(entered_year):
    """Запрещает пользователям выбирать год старше текущего."""
    current_year = dt.date.today().year
    if entered_year > current_year:
        raise serializers.ValidationError(
            ERROR_YEAR_FROM_FUTURE.format(entered_year, current_year))
    return entered_year


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            'Имя пользователя не может быть "me"'
        )
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError('Имя пользователя содержит '
                              'запрещенные символы')
