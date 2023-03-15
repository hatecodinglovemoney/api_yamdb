from django.contrib.auth import get_user_model
from django.db import models

from api_yamdb.settings import SLICE_STR_SYMBOLS

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='url',
        max_length=50,
        unique=True,
    )

    class Meta:
        default_related_name = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return f'{self.name[:SLICE_STR_SYMBOLS]}'


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='url',
        max_length=50,
        unique=True,
    )

    class Meta:
        default_related_name = 'genres'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return f'{self.name[:SLICE_STR_SYMBOLS]}'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    year = models.IntegerField(
        verbose_name='Год',
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='GenreTitle',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return f'{self.name[:SLICE_STR_SYMBOLS]}'


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        default_related_name = 'genre_title'

    def __str__(self) -> str:
        return f'{self.genre}-{self.title}'


class Reviews(models.Model):
    """Отзывы."""
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Aвтор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведения'
    )
    created = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created']
        default_related_name = 'reviews'
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title', 'text'],
                name='unique_text_title'
            ),
        )

    def __str__(self) -> str:
        return self.text[:SLICE_STR_SYMBOLS]


class Comments(models.Model):
    """Комментарии"""
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария'
    )
    reviews = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        verbose_name='Комментарии'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    created = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created']
        default_related_name = 'comments'
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'reviews', 'text'],
                name='unique_text_reviews'
            ),
        )

    def __str__(self) -> str:
        return self.text[:SLICE_STR_SYMBOLS]
