from rest_framework import serializers
from ..models import ArticleModel

class ArticleBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model=ArticleModel
        fields=['title', 'author', 'created_at']
        