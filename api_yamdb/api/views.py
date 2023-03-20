import django_filters
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, serializers, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb import settings

from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                             IsOwnerAdminModeratorOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignupSerializer, TitleGetSerializer,
                             TitlePostSerializer, TokenSerializer,
                             UserSerializer)
from reviews.models import Category, Genre, Review, Title

User = get_user_model()

EMAIL_HEADER = 'Код подтверждения'
EMAIL_TEXT = 'Ваш код подтверждения: {confirmation_code}'
EMAIL_ERROR = 'Данные имя пользователя или Email уже зарегистрированы'
CODE_ERROR = 'Введен неверный код.'


class UserViewSet(viewsets.ModelViewSet):
    """
    Администратор получает список пользователей, может создавать,
    удалять, редактировать пользователя. Пользователь по url 'users/me/'
    может получать и изменять свои данные, кроме поля 'Роль'.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')
    pagination_class = PageNumberPagination

    @action(methods=('get', 'patch'), detail=False, url_path='me',
            permission_classes=(IsAuthenticated,))
    def user_owner(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    """
    Пользователь отправляет свои 'username' и 'email' на 'auth/signup/ и
    получает код подтверждения на email.
    """
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    try:
        user, created = User.objects.get_or_create(username=username,
                                                   email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            EMAIL_HEADER,
            EMAIL_TEXT.format(confirmation_code=confirmation_code),
            settings.ADMIN_EMAIL,
            [user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    except IntegrityError:
        raise serializers.ValidationError(EMAIL_ERROR)


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_token(request):
    """
    Пользователь отправляет свои 'username' и 'confirmation_code'
    на 'auth/token/ и получает токен.
    """
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = str(AccessToken.for_user(user))
        return Response({'token': token}, status=status.HTTP_200_OK)
    raise serializers.ValidationError(CODE_ERROR)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки эндпоинтов:
    GET DETAIL, GET LIST, POST, PATCH, DELETE
    /titles/{title_id}/reviews/{review_id}/comments/,
    /titles/{titles_id}/reviews/{review_id}/comments/{comment_id}/
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.review.select_related('title', 'author')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки эндпоинтов:
    GET DETAIL, GET LIST, POST, PATCH, DELETE
    /titles/{title_id}/reviews/{review_id}/comments/,
    /titles/{titles_id}/reviews/{review_id}/comments/{comment_id}/
    """
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comment.select_related('review', 'author')

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class TitleFilter(django_filters.FilterSet):
    """
    Кастомный фильтр для Произведений.
    Решает проблему поиска по slug Жанра и Категории.
    """
    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='contains')
    category = django_filters.CharFilter(
        field_name='category__slug', lookup_expr='contains')
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='contains')
    year = django_filters.NumberFilter(
        field_name='year', lookup_expr='exact')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year')


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки эндпоинтов:
    GET DETAIL, GET LIST, POST, PATCH, DELETE
    /titles/, /titles/{titles_id}/
    """
    queryset = Title.objects.all().annotate(
        rating=Avg('review__score')
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitlePostSerializer


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    Вьюсет для обработки эндпоинтов:
    GET, POST, DELETE
    /genres/, /genres/{slug}/
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    Вьюсет для обработки эндпоинтов:
    GET, POST, DELETE
    /categories/, /categories/{slug}/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
