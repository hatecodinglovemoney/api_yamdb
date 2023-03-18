import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            'Имя пользователя не может быть "me"'
        )
    if not re.match(r'^[\w.@+-]+\z', value):
        raise ValidationError('Имя пользователя содержит '
                              'запрещенные символы')
