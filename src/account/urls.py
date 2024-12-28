from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django import views
from .views import UpdateUserProfile

urlpatterns = [
    path("user-profile/update/", UpdateUserProfile.as_view(), name="update-profile"),
]
