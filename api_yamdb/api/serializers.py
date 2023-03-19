import datetime as dt

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Genre, Title, Review, Comment
from users.validators import validate_username

User = get_user_model()

ERROR_YEAR_FROM_FUTURE = 'Год выпуска не может быть больше текущего!'


class UserSerializer(serializers.ModelSerializer):
    """Сериализация данных пользователя."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_unique_username(self, value):
        if (
            self.context.get('request').method == 'POST'
            and User.objects.filter(username=value).exists()
        ):
            raise ValidationError(
                'Пользователь с таким именем уже зарегестрирован.'
            )
        return validate_username(value)

    def validate_unique_email(self, value):
        if User.objects.filter(email=value).exists():
            return serializers.ValidationError(
                'Данный Email уже зарегистрирован')
        return value


class SignupSerializer(serializers.ModelSerializer):
    """Сериализация данных пользователя при регистрации."""
    username = serializers.CharField(required=True, max_length=150,
                                     validators=(validate_username,))
    email = serializers.EmailField(required=True, max_length=150)


class TokenSerializer(serializers.ModelSerializer):
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
        fields = '__all__'


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
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        """Запрещает пользователям оставлять повторные отзывы."""
        title = int(data['title'])
        author = self.context['request'].user
        if Review.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)
