from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from api_yamdb import settings
from api_yamdb.settings import SLICE_STR_SYMBOLS, SCORE_MIN, SCORE_MAX
from reviews.validators import validate_year, validate_username


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)

ERROR_SCORE_MIN_MAX = (
    f'Допустимы значения от {SCORE_MIN} до {SCORE_MAX}'
)


class User(AbstractUser):
    """Кастомная модель пользователя."""
    username = models.CharField(
        verbose_name='Имя пользователя',
        validators=(validate_username,),
        max_length=settings.USERNAME_LENGTH,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=settings.EMAIL_LENGTH,
        unique=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=settings.ROLE_LENGTH,
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
        max_length=settings.FIRST_NAME_LENGHT,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.LAST_NAME_LENGHT,
        blank=True
    )
    confirmation_code = models.CharField(
        max_length=settings.CONF_CODE_LENGHT,
        default=settings.CONF_CODE_DEFAULT
    )

    @property
    def is_user(self):
        """Обычный пользователь."""
        return self.role == USER

    @property
    def is_admin(self):
        """Пользователь с правами администратора."""
        return self.role == ADMIN or self.is_staff

    @property
    def is_moderator(self):
        """Пользователь с правами модератора."""
        return self.role == MODERATOR

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class CategoryOrGenreModel(models.Model):
    """Родительский класс для категорий и жанров."""
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.CATEGORY_NAME_LENGHT,
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=settings.CATEGORY_SLUG_LENGHT,
        unique=True,
    )


class Category(CategoryOrGenreModel):
    """Категория (Наследуется от AbstractModel)."""
    class Meta:
        default_related_name = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name[:SLICE_STR_SYMBOLS]


class Genre(CategoryOrGenreModel):
    """Жанр (Наследуется от AbstractModel)."""
    class Meta:
        default_related_name = 'genres'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name[:SLICE_STR_SYMBOLS]


class Title(models.Model):
    """Произведение."""
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.TITLE_NAME_LENGHT,
    )
    year = models.IntegerField(
        verbose_name='Год',
        validators=(validate_year,),
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
        return self.name[:SLICE_STR_SYMBOLS]


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


class ReviewOrCommentModel(models.Model):
    """Родительский класс для отзывов и комментариев."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Aвтор',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:SLICE_STR_SYMBOLS]


class Review(ReviewOrCommentModel):
    """Отзывы пользователей (Наследуется от ReviewOrCommentModel)."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(SCORE_MIN, ERROR_SCORE_MIN_MAX),
            MaxValueValidator(SCORE_MAX, ERROR_SCORE_MIN_MAX),
        ],
    )

    class Meta:
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_title'),
        )


class Comment(ReviewOrCommentModel):
    """Комментарии пользователей (Наследуется от ReviewOrCommentModel)."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
