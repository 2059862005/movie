from django.urls import path, include
from rest_framework.routers import DefaultRouter
from movie.views import MovieViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'', MovieViewSet, basename='movie')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
