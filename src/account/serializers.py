from rest_framework import serializers
from .models import CustomUser, UserProfile

class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'fullname']

class UserReadSerializer(UserBaseSerializer):
    ...


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()
    class Meta:
        model= UserProfile
        fields =['birthday', 'profile_pic', 'user']


    def update(self, instance, validated_data):
        # Extract nested user data and collect them together
        user_data = validated_data.pop('user', None)
        
        # Update the UserProfile instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update the related CustomUser instance
        if user_data:
            custom_user = instance.user  # Get the associated CustomUser instance
            custom_user.email = user_data.get('email', custom_user.email)
            custom_user.fullname = user_data.get('fullname', custom_user.fullname)
            custom_user.save()

        return instance