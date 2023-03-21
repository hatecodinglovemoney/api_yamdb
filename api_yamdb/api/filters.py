import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """
    Кастомный фильтр для Произведений.
    Решает проблему поиска по slug Жанра и Категории.
    """
    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='contains')
    category = django_filters.CharFilter(
        field_name='category__slug', lookup_expr='contains')
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='contains')
    year = django_filters.NumberFilter(
        field_name='year', lookup_expr='exact')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year')
