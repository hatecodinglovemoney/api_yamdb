from reviews.models import Reviews, Comments
from rest_framework import viewsets

from .serializers import (ReviewsSerializer,
                          CommentsSerializer)


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
