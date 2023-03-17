from django.contrib.auth import get_user_model
from django.db import models

from api_yamdb.settings import SLICE_STR_SYMBOLS

User = get_user_model()

RATING_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)


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
    rating = models.IntegerField(
        verbose_name='Рейтинг произведения',
        blank=True,
        null=True,
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return f'{self.name[:SLICE_STR_SYMBOLS]}-score {self.score}'


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


class Review(models.Model):
    """Отзывы пользователей."""
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
        verbose_name='Произведение'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        on_delete=models.CASCADE,
        choices=RATING_CHOICES,
        null=True,
    )

    class Meta:
        ordering = ['-pub_date']
        default_related_name = 'review'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title', 'text'],
                name='unique_text_title'
            ),
        )

    def __str__(self) -> str:
        return self.text[:SLICE_STR_SYMBOLS]


class Comment(models.Model):
    """Комментарии пользователей."""
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария'
    )
    reviews = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        default_related_name = 'comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'review', 'text'],
                name='unique_text_reviews'
            ),
        )

    def __str__(self) -> str:
        return self.text[:SLICE_STR_SYMBOLS]
