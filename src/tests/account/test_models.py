import pytest
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.utils import IntegrityError
import os
from account.models import UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.mark.django_db 
class TestCustomUserModel:

    @pytest.mark.django_db  # for connection with the database
    def test_create_user(self):
        """Test that creating a new User and saving it to database"""
        email='test@gmail.com'
        fullname='test1'
        password="123456"

        user=get_user_model().objects.create_user(
            email=email,
            fullname=fullname,
            password=password
        )

        assert user.email == email    # check if the created user's email is same with the email we sent
        assert user.fullname == fullname
        assert user.check_password(password) == True
        assert user.is_staff == False
        assert user.is_superuser == False
        assert user.is_active == True


    @pytest.mark.django_db  # for connection with the database
    def test_create_super_user(self):
        """Test that creating Super User and saving to database"""
        email='test@gmail.com'
        fullname='test1'
        password="123456"

        user=get_user_model().objects.create_superuser(
            email=email,
            fullname=fullname,
            password=password
        )

        assert user.email == email    # check if the created user's email is same with the email we sent
        assert user.fullname == fullname
        assert user.check_password(password) == True
        assert user.is_staff == True
        assert user.is_superuser == True
        assert user.is_active == True


    @pytest.mark.django_db 
    def test_create_user_without_email(self):
        """"Test creating a new user without an email"""

        with pytest.raises(ValueError, match=str(_("The Email must be set"))):
            get_user_model().objects.create_user(email="", 
                                                 fullname="Test2", 
                                                 password="1234")
            
    @pytest.mark.django_db 
    def test_create_user_without_fullname(self):
        """"Test creating a new user without a fullname"""

        with pytest.raises(ValueError, match=str(_("The Fullname must be set"))):
            get_user_model().objects.create_user(email="test3@gmail.com", 
                                                 fullname="", 
                                                 password="1234")
            
    def test_unique_email(self):
        """Test creating a new user with a repeated email"""
        get_user_model().objects.create_user(email="test1@gmail.com", 
                                             fullname='test1', 
                                             password='1234')
        
        with pytest.raises(IntegrityError):
            get_user_model().objects.create_user(email="test1@gmail.com", 
                                             fullname='test2', 
                                             password='1234')
            
    def test_user_string_representation(self):
        """Test user's __str__ method"""
        user = get_user_model().objects.create_user(email="test1@gmail.com", 
                                             fullname='test1', 
                                             password='1234')
        assert str(user) == user.email

    def test_super_user_with_no_staff_status(self):
        """Test creating a super user with is_staff = False"""
        with pytest.raises(ValueError, match=str(_("Superuser must have is_staff=True."))):
            get_user_model().objects.create_superuser(email="test1@gmail.com", 
                                             fullname='test2', 
                                             password='1234',
                                             is_staff = False)



class TestUserProfileModel:
    @pytest.mark.django_db
    def test_image_uploading_to_user_profile(self):

        user = get_user_model().objects.create_user(
                                email="testimage@example.com",
                                fullname="Test Image",
                                password="1234"
                            )
    
        # Simulate an image upload
        image_path = os.path.join(os.path.dirname(__file__), "profile_pic_test.jpg")
        with open(image_path, "wb") as img_file:
            img_file.write(b"This is a test image content")  
    
        image = SimpleUploadedFile(
            name="profile_pic_test.jpg",
            content=open(image_path, "rb").read(),
            content_type="image/jpeg"
        )

        # Update the user profile with the image
        profile = user.profile
        profile.profile_pic = image
        profile.save()

        # Reload the profile from the database
        updated_profile = UserProfile.objects.get(user=user)

        # Assertions
        assert "profile_pic_test" in updated_profile.profile_pic.name  # Check that the base name is in the uploaded file name
        assert updated_profile.profile_pic.name.startswith("user_profile_pictures/")  # Ensure it was uploaded to the correct directory
        assert os.path.exists(updated_profile.profile_pic.path)  # Ensure the file exists on the disk

        # Clean up the uploaded file
        updated_profile.profile_pic.delete(save=False)
        os.remove(image_path)
        