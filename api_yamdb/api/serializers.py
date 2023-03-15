from rest_framework import serializers

from reviews.models import Reviews, Comments


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        field = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        field = '__all__'
