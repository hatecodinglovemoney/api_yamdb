from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend


from api.serializers import (ReviewsSerializer,
                             CommentsSerializer,
                             TitleGetSerializer,
                             TitlePostSerializer, GenreSerializer, CategorySerializer)
from reviews.models import Reviews, Comments, Title, Genre, Category


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre__slug', 'category__slug')
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitlePostSerializer


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = None


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = None
