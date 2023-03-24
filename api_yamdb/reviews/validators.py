import re
import datetime as dt

from rest_framework import serializers
from django.core.exceptions import ValidationError

ERROR_YEAR_FROM_FUTURE = ('Год выпуска ({entered_year}), не может '
                          'быть больше текущего ({current_year})!')
LEGAL_CHARACTERS = re.compile(r'[\w.@+-]')
LEGAL_CHARACTERS_ERROR = ('Нельзя использовать символ(ы): '
                          '{forbidden_chars} в имени пользователя.')
INVALID_NAMES = ('me',)
INVALID_NAMES_ERROR = 'Имя пользователя не может быть {value}'


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
    if value in INVALID_NAMES:
        raise ValidationError(INVALID_NAMES_ERROR.format(value=value))
    forbidden_chars = ''.join(set(LEGAL_CHARACTERS.sub('', value)))
    if forbidden_chars:
        raise ValidationError(
            LEGAL_CHARACTERS_ERROR.format(forbidden_chars=forbidden_chars)
        )
