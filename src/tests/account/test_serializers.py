import pytest
from django.contrib.auth import get_user_model
from account.serializers import UserProfileSerializer
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_update_user_profile(user):
    """Test using UserProfileSerializer to update user profile"""

    user_new_data={
        "email":"new_email@gmail.com",
        "fullname":"new_test"
    }

    profile_new_data={
        "birthday":"1999-03-08",
        "user":user_new_data
    }

    serializer=UserProfileSerializer(user.profile, data=profile_new_data)

    assert serializer.is_valid(), serializer.errors
    updated_user_profile=serializer.save()

    assert updated_user_profile.user.email == user_new_data["email"]
    assert updated_user_profile.user.fullname == user_new_data["fullname"]
    assert str(updated_user_profile.birthday) == profile_new_data["birthday"]


@pytest.mark.django_db
def test_update_user_profile_with_invalid_email(user):
    """Test using UserProfileSerializer to update user profile with an invalid email"""

    user_new_data={
        "email":"new_emailgmail.com",
        "fullname":"new_test"
    }

    profile_new_data={
        "birthday":"1999-03-08",
        "user":user_new_data
    }

    serializer=UserProfileSerializer(user.profile, data=profile_new_data)

    # Ensure that the serializer is not valid due to the invalid email
    assert not serializer.is_valid()

    # Check if the email field inside the 'user' nested field has the correct error message
    assert 'user' in serializer.errors
    assert 'email' in serializer.errors['user']

    
