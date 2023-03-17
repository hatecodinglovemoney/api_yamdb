from django.urls import include, path
from rest_framework import routers


from api.views import (CategoryViewSet,
                       CommentViewSet,
                       GenreViewSet,
                       ReviewViewSet,
                       TitleViewSet)


v1_router = routers.DefaultRouter()

v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('review', ReviewViewSet, basename='review')
v1_router.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
