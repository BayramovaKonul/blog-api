from rest_framework import serializers
from ..models import CategoryModel

class CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['name', 'slug']

class CategoryWriteSerializer(CategoryReadSerializer):
    ...
