from django.urls import include, path
from rest_framework import routers


from api.views import (CategoryViewSet,
                       CommentViewSet,
                       GenreViewSet,
                       ReviewViewSet,
                       TitleViewSet)
from api.views import UserViewSet, signup, get_token

v1_router = routers.DefaultRouter()

v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/review/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)
v1_router.register('users', UserViewSet, basename='users')

auth_path = [
    path('auth/signup/', signup),
    path('auth/token/', get_token)
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include(auth_path))
]
