from django.urls import include, path
from rest_framework import routers

from api.views import ReviewsViewSet, CommentsViewSet

v1_router = routers.DefaultRouter()

v1_router.register('reviews/', ReviewsViewSet, basename='reviews')
v1_router.register('comments/', CommentsViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
