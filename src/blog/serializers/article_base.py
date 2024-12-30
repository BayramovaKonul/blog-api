from rest_framework import serializers
from ..models import ArticleModel
from account.serializers import UserReadSerializer
from .categories import CategoryReadSerializer
import mimetypes
from django.core.exceptions import ValidationError

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
    

       
        
    def validate_picture(self, value):
        # Guess the MIME type of the uploaded file based on its extension
        mime_type, encoding = mimetypes.guess_type(value.name)
        
        # Allowed image MIME types
        valid_mime_types = ['image/jpeg', 'image/png']
        
        # Check if the file's MIME type is in the allowed list
        if mime_type not in valid_mime_types:
            raise ValidationError(f"Only image files are allowed. Detected file type: {mime_type}")
        
        return value

class ArticleUpdateSerializer(ArticleWriteSerializer):
        ...