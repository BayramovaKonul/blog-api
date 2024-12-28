from rest_framework import serializers
from ..models import BookMarkModel
from account.serializers import UserReadSerializer
from ..serializers import ArticleReadSerializer

class BookMarkSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()
    article = ArticleReadSerializer()

    class Meta:
        model=BookMarkModel
        fields=['user', 'article']
        
