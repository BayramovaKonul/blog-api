from rest_framework import serializers
from ..models import BookMarkModel
from account.serializers import UserReadSerializer
from ..serializers import ArticleReadSerializer

class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model=BookMarkModel
        fields=['article']
        extra_kwargs = {'article': {'required': False}}  # Article is optional in request data
        
