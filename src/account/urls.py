from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django import views
from .views import (UpdateUserProfile, UpdateUserProfilePicture, RegisterUserView, 
                    UserFollowerView, MyFollowersView, ResetPasswordView, RequestPasswordResetView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("profile/update/", UpdateUserProfile.as_view(), name="update-profile"),
    path("picture/update/", UpdateUserProfilePicture.as_view(), name="update-picture"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterUserView.as_view(), name='register'),
    path('follower/<int:following_id>/', UserFollowerView.as_view(), name='follow_delete'),
    path('myfollowers', MyFollowersView.as_view(), name='my_followers'),
    path('request-reset-password/', RequestPasswordResetView.as_view(), name='request-reset-password'),
    path('confirm-reset-password/', ResetPasswordView.as_view(), name='confirm-reset-password'),
]

