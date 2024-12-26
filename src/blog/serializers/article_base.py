from rest_framework import serializers
from ..models import ArticleModel
from account.serializers import UserReadSerializer
from .categories import CategoryReadSerializer
class ArticleReadSerializer(serializers.ModelSerializer):
    author = UserReadSerializer()
    categories = CategoryReadSerializer(many=True)
    class Meta:
        model=ArticleModel
        fields=['title', 'slug', 'content', 'author', 'categories', 'published_at', 'created_at']
        
class ArticleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=ArticleModel
        fields=['title', 'slug', 'content', 'categories', 'picture', 'published_at']

    # before validation starts, this part works first
    # def to_internal_value (self, data):
    #     return super().to_internal_value(data)
    

class ArticleUpdateSerializer(ArticleWriteSerializer):
        ...