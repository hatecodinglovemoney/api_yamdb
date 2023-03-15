import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre, Title, Reviews, Comments

ERROR_YEAR_FROM_FUTURE = 'Год выпуска не может быть больше текущего!'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        field = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        field = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        field = '__all__'

    def validate_year(self, value):
        year = dt.date.today().year
        if value < year:
            raise serializers.ValidationError(ERROR_YEAR_FROM_FUTURE)
        return value


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        field = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        field = '__all__'
