from django.urls import include, path
from rest_framework import routers

from api.views import TitleViewSet, GenreViewSet, CategoryViewSet

v1_router = routers.DefaultRouter()

v1_router.register('titles/', TitleViewSet, basename='title')
v1_router.register('genres/', GenreViewSet, basename='genre')
v1_router.register('categories/', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
