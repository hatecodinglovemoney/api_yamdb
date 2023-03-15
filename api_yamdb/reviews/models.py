from django.db import models

from api_yamdb.settings import SLICE_STR_SYMBOLS


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
                fields=['author', 'title'],
                name='unique_author_title'
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

    def __str__(self) -> str:
        return self.text[:SLICE_STR_SYMBOLS]
