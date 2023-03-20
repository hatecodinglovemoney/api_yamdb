from django.db import models
from django.contrib.auth.models import AbstractUser

from api_yamdb.settings import SLICE_STR_SYMBOLS
from reviews.validators import validate_username


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

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class User(AbstractUser):
    """Кастомная модель пользователя."""
    username = models.CharField(
        verbose_name='Имя пользователя',
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )

    @property
    def is_user(self):
        """Обычный пользователь."""
        return self.role == USER

    @property
    def is_admin(self):
        """Пользователь с правами администратора."""
        return self.role == ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        """Пользователь с правами модератора."""
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    """Категория."""
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
    """Жанр."""
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
    """Произведение."""
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
    """Жанр произведения."""
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
                fields=['author', 'title'],
                name='unique_author_title'),
        )

    def __str__(self) -> str:
        return self.text[:SLICE_STR_SYMBOLS]


class Comment(models.Model):
    """Комментарии пользователей."""
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария'
    )
    review = models.ForeignKey(
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
                fields=['author', 'text'],
                name='unique_text'
            ),
        )

    def __str__(self) -> str:
        return self.text[:SLICE_STR_SYMBOLS]
