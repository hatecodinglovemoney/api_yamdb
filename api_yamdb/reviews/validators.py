import re
import datetime as dt

from rest_framework import serializers
from django.core.exceptions import ValidationError

from api_yamdb import settings

ERROR_YEAR_FROM_FUTURE = ('Год выпуска ({entered_year}), не может '
                          'быть больше текущего ({current_year})!')
LEGAL_CHARACTERS_ERROR = ('Нельзя использовать символ(ы): '
                          '{forbidden_chars} в имени пользователя.')
FORBIDDEN_NAMES_ERROR = 'Имя пользователя не может быть {value}'


def validate_year(entered_year):
    """Запрещает пользователям выбирать год старше текущего."""
    current_year = dt.date.today().year
    if entered_year > current_year:
        raise serializers.ValidationError(
            ERROR_YEAR_FROM_FUTURE.format(
                entered_year=entered_year,
                current_year=current_year
            )
        )
    return entered_year


def validate_username(value):
    if value in settings.FORBIDDEN_NAMES:
        raise ValidationError(FORBIDDEN_NAMES_ERROR.format(value=value))
    forbidden_chars = ''.join(set(re.compile(
        settings.LEGAL_CHARACTERS).sub('', value)))
    if forbidden_chars:
        raise ValidationError(
            LEGAL_CHARACTERS_ERROR.format(forbidden_chars=forbidden_chars)
        )
