from django.shortcuts import render
from .serializers import UserReadSerializer, UserProfileSerializer, ProfilePictureSerializer, UserRegisterSerializer, UserFollowerWriteSerializer, UserFollowerReadSerializer
from .models import CustomUser, UserProfile, UserFollowerModel
from django.http import HttpResponse
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.permissions import AllowAny
from blog.pagination import MyPagination
from drf_yasg.utils import swagger_auto_schema

class UpdateUserProfile(APIView):
    @swagger_auto_schema(
        request_body=UserProfileSerializer,
        responses={
            200: UserProfileSerializer,
            400: 'Bad request, invalid data.',
        }
    )
    def patch(self, request):
        user_profile = request.user.profile # profile is a related name
        # Initialize the serializer
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            

class UpdateUserProfilePicture(APIView):
    @swagger_auto_schema(
        request_body=ProfilePictureSerializer,
        responses={
            200: ProfilePictureSerializer,
            400: 'Bad request, invalid data.',
        }
    )
    def patch(self, request):
        user_profile = request.user.profile # profile is a related name
        # Initialize the serializer
        serializer = ProfilePictureSerializer(user_profile, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterUserView(APIView):
    permission_classes = [AllowAny]  # Allow access without authentication

    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={
            200: UserRegisterSerializer,
            400: 'Bad request, invalid data.',
        }
    )
    def post(self, request):
        serializer= UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class UserFollowerView(APIView):
    def post(self, request, following_id):
        follower=request.user

        if UserFollowerModel.objects.filter(follower=follower, following=following_id).exists():
            return Response("You have already followed this user")
        
        serializer=UserFollowerWriteSerializer(data={"following":following_id})
        if serializer.is_valid(raise_exception=True):
            serializer.save(follower=follower)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def delete(self, request, following_id):
        following=get_object_or_404(UserFollowerModel, following=following_id)
        following.delete()
        return Response(
            data={"success": True},
            status=status.HTTP_204_NO_CONTENT
        )
        
    def get(self, request):
        follower_fullname=request.query_params.get('follower_fullname')
        my_followers=UserFollowerModel.objects.filter(following=request.user)

        if follower_fullname:
            my_followers=my_followers.filter(follower__fullname__icontains=follower_fullname)

        paginator=MyPagination()
        paginated_followers=paginator.paginate_queryset(my_followers, request)
        serializer=UserFollowerReadSerializer(paginated_followers,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 