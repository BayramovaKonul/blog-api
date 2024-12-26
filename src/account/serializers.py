from rest_framework import serializers
from .models import CustomUser

class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'fullname']

class UserReadSerializer(UserBaseSerializer):
    ...