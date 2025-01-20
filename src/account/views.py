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
from drf_yasg import openapi
from .throttling import UserRegisterThrottle

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
    throttle_classes = [UserRegisterThrottle]

    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={
            201: UserRegisterSerializer,
            400: 'Bad request, invalid data.',
        }
    )
    def post(self, request):
        serializer= UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class UserFollowerView(APIView):
    @swagger_auto_schema(
        responses={
            403: 'Forbidden:You have already followed this user',
            201: 'User followed successfully',
        }
    )
    def post(self, request, following_id):
        follower=request.user
        if UserFollowerModel.objects.filter(follower=follower, following=following_id).exists():
            return Response(
                {"detail": "You have already followed this user."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer=UserFollowerWriteSerializer(data={"following":following_id})
        if serializer.is_valid(raise_exception=True):
            serializer.save(follower=follower)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    @swagger_auto_schema(
        responses={
            204: 'User was excluded from the follower list',
        }
    )
    def delete(self, request, following_id):
        following=get_object_or_404(UserFollowerModel, following=following_id)
        following.delete()
        return Response(
            data={"success": True},
            status=status.HTTP_204_NO_CONTENT
        )
        
class MyFollowersView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "follower_fullname",
                openapi.IN_QUERY,
                description="Filter followers by full name (case-insensitive match).",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Specify the page number for pagination.",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: openapi.Response(
                description="A list of followers.",
                schema=UserFollowerReadSerializer(many=True),
            ),
            400: "Bad Request",
        }
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
 