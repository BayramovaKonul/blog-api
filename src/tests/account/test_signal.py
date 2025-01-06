import pytest
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.utils import IntegrityError
from account.models import UserProfile

@pytest.mark.django_db 

def test_create_user_profile_using_signal():
    """Test that creating a user profile automatically after user registers"""
    email='test2@gmail.com'
    fullname='test2'
    password="1234"

    user=get_user_model().objects.create_user(
        email=email,
        fullname=fullname,
        password=password
    )

    profile=UserProfile.objects.get(user=user)

    assert profile.user == user  # Ensure the profile is linked to the correct user
    assert profile.user.email == email  # Check the user's email matches
    assert profile.user.fullname == fullname  # Check the user's fullname matches