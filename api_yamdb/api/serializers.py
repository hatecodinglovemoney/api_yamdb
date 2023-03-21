from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

from reviews.validators import validate_year, validate_username

User = get_user_model()

ERROR_REPEAT_REVIEW = 'Вы уже оставляли отзыв на это произведение'


class UserSerializer(serializers.ModelSerializer):
    """Сериализация данных пользователя."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignupSerializer(serializers.ModelSerializer):
    """Сериализация данных пользователя при регистрации."""
    username = serializers.CharField(required=True, max_length=150,
                                     validators=(validate_username,))
    email = serializers.EmailField(required=True, max_length=254,)

    class Meta:
        model = User
        fields = ('username', 'email',)


class TokenSerializer(serializers.Serializer):
    """Сериализация данных для получения токена."""
    username = serializers.CharField(required=True, max_length=150,
                                     validators=(validate_username,))
    confirmation_code = serializers.CharField(required=True)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализация данных для эндпоинтов Жанра."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация данных для эндпоинтов Категорий."""
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleGetSerializer(serializers.ModelSerializer):
    """
    Сериализация данных для GET-запроса
    к эндпоинту Произведений.
    """
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category', 'rating'
        )
        read_only_fields = fields


class ObjectField(serializers.SlugRelatedField):
    """
    Кастомное поле для правильного отображения
    полей Жанр и Категория после POST-запроса
    к эндпоинту Произведений.
    """
    def to_representation(self, obj):
        return {
            'name': obj.name,
            'slug': obj.slug,
        }


class TitlePostSerializer(serializers.ModelSerializer):
    """
    Сериализация данных для POST и PATCH запросов
    к эндпоинту Произведений.
    """
    genre = ObjectField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all())
    category = ObjectField(
        many=False,
        slug_field='slug',
        queryset=Category.objects.all())
    year = serializers.IntegerField(
        validators=(validate_year,),
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация данных для эндпоинтов Отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Запрещает пользователям оставлять повторные отзывы."""
        if not self.context.get('request').method == 'PATCH':
            if Review.objects.filter(
                author=self.context.get('request').user,
                title=get_object_or_404(
                    Title, id=self.context.get('view').kwargs.get('title_id')
                )
            ).exists():
                raise serializers.ValidationError(ERROR_REPEAT_REVIEW)
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация данных для эндпоинтов Коментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
