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
    username = serializers.CharField(required=True, max_length=150,
                                     validators=(validate_username,))
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignupSerializer(serializers.ModelSerializer):
    """Сериализация данных пользователя при регистрации."""
    username = serializers.CharField(required=True, max_length=150,
                                     validators=(validate_username,))
    email = serializers.EmailField(required=True, max_length=254)

    def validate_unique_username(self, value):
        if (
            self.context.get('request').method == 'POST'
            and User.objects.filter(username=value).exists()
        ):
            raise ValidationError(
                'Пользователь с таким именем уже зарегестрирован.'
            )
        return value

    def validate_unique_email(self, value):
        if User.objects.filter(email=value).exists():
            return ValidationError(
                'Данный Email уже зарегистрирован')
        return value

    class Meta:
        model = User
        fields = ('username', 'email',)


class TokenSerializer(serializers.Serializer):
    """Сериализация данных для получения токена."""
    username = serializers.CharField(required=True, max_length=150,
                                     validators=(validate_username,))
    confirmation_code = serializers.CharField(required=True)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='slug',
        queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        """Запрещает пользователям выбирать год выше текущего."""
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(ERROR_YEAR_FROM_FUTURE)
        return value


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
