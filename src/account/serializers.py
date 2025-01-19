from rest_framework import serializers
from .models import CustomUser, UserProfile, UserFollowerModel
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.validators import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

User= get_user_model()
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
        fields =['birthday', 'user']


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
    
class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserProfile
        fields =['profile_pic']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add new fields to show in the body of payload
        token['email'] = user.email
        if user.is_staff and user.is_superuser:
            token['user_type'] = "admin"
        elif user.is_staff:
            token['user_type'] = "staff"
        else:
            token['user_type'] = "regular user"

        return token
    
    
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add new fields to show in the body of payload
        token['email'] = user.email
        if user.is_staff and user.is_superuser:
            token['user_type'] = "admin"
        elif user.is_staff:
            token['user_type'] = "staff"
        else:
            token['user_type'] = "regular user"

        return token

        return token
    
class UserRegisterSerializer(serializers.ModelSerializer):
    # use them when writing data to the database, but don't include in response
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['fullname', 'email', 'password1', 'password2']

    def validate(self, data):
        fullname = data.get('fullname')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')

        # Check for unique email
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})

        if password1 != password2:
            raise serializers.ValidationError({"password2": "Passwords must match."})

        # If passwords match, remove password2 and set password1 to password.
        data['password'] = make_password(password1)
        data.pop('password1')
        data.pop('password2')
        return data
    
class UserFollowerWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserFollowerModel
        fields=['following']

class UserFollowerReadSerializer(serializers.ModelSerializer):
    follower_id = serializers.IntegerField(source='follower.id', read_only=True)
    follower_email = serializers.EmailField(source='follower.email', read_only=True)
    follower_fullname = serializers.CharField(source='follower.fullname', read_only=True)
    # profile is a related name, since profile picture is saved in UserprofileModel
    follower_profile_pic = serializers.ImageField(source='follower.profile.profile_pic', read_only=True)
    class Meta:
        model=UserFollowerModel
        fields = ['follower_id', 'follower_email', 'follower_fullname', 'follower_profile_pic']


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value


# class ResetPasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(required=True, write_only=True)
#     new_password = serializers.CharField(required=True, write_only=True, min_length=8)
#     confirm_password = serializers.CharField(required=True, write_only=True)

#     def validate_old_password(self, value):
#         user = self.context.get('user')  # Retrieve user from context
#         print(user.password)
#         if not check_password(value, user.password):
#             raise serializers.ValidationError("The old password is incorrect.")
#         return value

#     def validate(self, data):
#         new_password = data.get('new_password')
#         confirm_password = data.get('confirm_password')

#         if new_password != confirm_password:
#             raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
#         return data

#     def save(self, **kwargs):
#         user = self.context.get('user')  # Retrieve user from context
#         user.set_password(self.validated_data['new_password'])
#         user.save()

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def save(self, **kwargs):
        user = self.context.get('user')  # Retrieve user from context
        user.set_password(self.validated_data['new_password'])
        user.save()
