from rest_framework import serializers
from ..models import ArticleModel

class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=ArticleModel
        fields=['title', 'slug', 'author', 'content', 'categories', 'published_at']
    
