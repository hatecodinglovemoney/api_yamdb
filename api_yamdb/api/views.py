from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


from api.serializers import (CategorySerializer,
                             CommentSerializer,
                             GenreSerializer,
                             ReviewSerializer,
                             TitleGetSerializer,
                             TitlePostSerializer)
from reviews.models import Category, Genre, Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.review.select_related('title', 'author')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        reviews = Review.objects.select_related('title')
        scores = reviews.values_list('score', flat=True)
        scores = list(scores)
        scores.append(serializer.validated_data['score'])
        if scores == 0:
            return 'Оценок ещё нет'
        rating = sum(scores) / len(scores)
        title.rating = round(rating)
        title.save()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comment.select_related('review', 'author')

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre__slug', 'category__slug')
    pagination_class = PageNumberPagination

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
    pagination_class = PageNumberPagination


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
