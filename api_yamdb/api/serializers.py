import datetime as dt

from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.validators import validate_username

User = get_user_model()

ERROR_YEAR_FROM_FUTURE = 'Год выпуска не может быть больше текущего!'
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
    """Сериализация данных для эндпоитов Жанра."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация данных для эндпоитов Категорий."""
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleGetSerializer(serializers.ModelSerializer):
    """
    Сериализация данных для GET-запроса
    к эндпоиту Произведений.
    """
    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category', 'rating'
        )


class ObjectField(serializers.SlugRelatedField):
    """
    Кастомное поле для правильного отображения
    полей Жанр и Категория после POST-запроса
    к эндпоиту Произведений.
    """
    def to_representation(self, obj):
        return {'name': obj.name,
                'slug': obj.slug}


class TitlePostSerializer(serializers.ModelSerializer):
    """
    Сериализация данных для POST и PATCH запросов
    к эндпоиту Произведений.
    """
    genre = ObjectField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all())
    category = ObjectField(
        many=False,
        slug_field='slug',
        queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, entered_year):
        """Запрещает пользователям выбирать год старше текущего."""
        if entered_year > dt.date.today().year:
            raise serializers.ValidationError(ERROR_YEAR_FROM_FUTURE)
        return entered_year


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация данных для эндпоитов Отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Title.objects.all(),
        required=False
    )

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Запрещает пользователям оставлять повторные отзывы."""
        author = self.context['request'].user
        title_id = self.context.get('view').kwargs.get('title_id')
        if (self.context['request'].method == 'POST'
                and Review.objects.filter(
                    title_id=title_id, author=author).exists()):
            raise serializers.ValidationError(ERROR_REPEAT_REVIEW)
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация данных для эндпоитов Коментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)
