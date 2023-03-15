from rest_framework import serializers

from reviews.models import Category, Genre, Title


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
