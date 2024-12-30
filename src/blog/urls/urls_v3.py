from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.views_v3 import ArticleViewSet

# Initialize the router
router = DefaultRouter()

# Register the ArticleViewSet to the router
router.register(r'articles', ArticleViewSet, basename='article')

# Define the URL patterns using the router
urlpatterns = [
    path('', include(router.urls)),  # Include all the routes generated by the router
]