from django.shortcuts import render
from .serializers import (UserReadSerializer, UserProfileSerializer, ProfilePictureSerializer, 
                          UserRegisterSerializer, UserFollowerWriteSerializer, UserFollowerReadSerializer, 
                          RequestPasswordResetSerializer, ForgotPasswordSerializer)
from .models import CustomUser, UserProfile, UserFollowerModel, ForgotPasswordTokenModel
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
from .throttling import UserRegisterThrottle, AddFollowerThrottle
from .throttling import UserRegisterThrottle
from django.contrib.auth import get_user_model
from .task import send_password_reset_email
User= get_user_model()

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
    throttle_scope = 'update_profile'  # user can update his profile only 5 times in an hour
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
    throttle_classes = [AddFollowerThrottle] 
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
        following.delete() # it is better to change is_used field to True instead of deleting. Keep track on them
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
 

@swagger_auto_schema(
        request_body=RequestPasswordResetSerializer,
        responses={
            200: 'Password reset email sent successfully.',
            400: 'Bad request, invalid data.',
    }
    )
class RequestForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            # Create a new token for the user
            user = User.objects.get(email=email)
            token = ForgotPasswordTokenModel.objects.create(user=user)
            # Send password reset email in the background
            reset_link = f"http://example.com/forgot-password?token={token.token}"
            send_password_reset_email.delay(email, reset_link)

            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@swagger_auto_schema(
        request_body=ForgotPasswordSerializer,
        responses={
            200: 'Password reset is successfully.',
            400: 'Bad request, invalid data.',
    }
    )
class ConfirmForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        token = request.query_params.get('token')

        # Check if token exists and is valid
        reset_token = ForgotPasswordTokenModel.objects.filter(token=token).first()

        if not reset_token:
            return Response({"message": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        if reset_token.is_expired():
            return Response({"message": "The token has expired."}, status=status.HTTP_400_BAD_REQUEST)

        user = reset_token.user

        # Pass user to the serializer to check passwords
        serializer = ForgotPasswordSerializer(data=request.data, context={'user': user})

        if serializer.is_valid():
            serializer.save()
            # Invalidate the token by deleting it
            reset_token.delete()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(
#         request_body=ResetPasswordSerializer,
#         responses={
#             200: 'Password reset is successfully.',
#             400: 'Bad request, invalid data.',
#     }
#     )
# class ConfirmPasswordResetView(APIView):
#     def post(self, request):
#         user=request.user
#         serializer = ResetPasswordSerializer(data=request.data, context={'user': user})
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)