from rest_framework import serializers
from ..models import ArticleModel
from account.serializers import UserReadSerializer
from .categories import CategoryReadSerializer
class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserReadSerializer()
    categories = CategoryReadSerializer(many=True)
    class Meta:
        model=ArticleModel
        fields=['title', 'slug', 'author', 'content', 'categories', 'published_at']
    
