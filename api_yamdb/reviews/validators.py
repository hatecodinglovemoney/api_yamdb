import datetime as dt

from rest_framework import serializers

ERROR_YEAR_FROM_FUTURE = 'Вы ввели {} год, но год выпуска не может быть больше текущего ({})!'


def validate_year(entered_year):
    """Запрещает пользователям выбирать год старше текущего."""
    current_year = dt.date.today().year
    if entered_year > current_year:
        raise serializers.ValidationError(
            ERROR_YEAR_FROM_FUTURE.format(entered_year, current_year))
    return entered_year
