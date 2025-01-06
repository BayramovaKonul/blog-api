import pytest 
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
def test_token_obtain_view_with_valid_credentials(user, anonymous_client):
    """Test getting access and refresh token using login credentials"""
    # where the request sent - use url_name
    url = reverse("token_obtain_pair")
    # user credentials
    data={
        "email":user.email,
        "password":"1234"
    }
    # client sent a post request to the url using his credentials
    res=anonymous_client.post(url, data=data, format='json')

    assert res.status_code==status.HTTP_200_OK

    assert 'access' in res.data
    assert 'refresh' in res.data

    assert len(res.data["access"]) > 0
    assert len(res.data["refresh"]) > 0


@pytest.mark.django_db
def test_token_refresh_view_with_valid_credentials(user, authenticated_client):
    """Test getting access token using logged in user's refresh token"""
    url=reverse("token_refresh")

    client, refresh = authenticated_client
    # payload part
    data = {
        "refresh":str(refresh)
    }

    res=client.post(url, data=data, format='json')

    assert res.status_code==status.HTTP_200_OK
    assert 'access' in res.data
    assert len(res.data["access"]) > 0


@pytest.mark.django_db
def test_register_view_with_valid_credentials(anonymous_client):
    """Test that user registers with valid credentials """
    url = reverse("register")

    data={
        "email":'test3@gmail.com',
        "fullname": 'test3',
        "password1": "1234",
        "password2": "1234"
    }

    res = anonymous_client.post(url, data=data,format='json')

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["email"] == data["email"]
    assert res.data["fullname"] == data["fullname"]

@pytest.mark.django_db
def test_register_view_with_unmatched_passwords(anonymous_client):
    """Test that it raises error when entered passwords don't match """
    url = reverse("register")

    data={
        "email":'test3@gmail.com',
        "fullname": 'test3',
        "password1": "1234",
        "password2": "12345"
    }

    res = anonymous_client.post(url, data=data,format='json')

    assert not res.status_code == status.HTTP_201_CREATED
    assert res.data['password2'] == ["Passwords must match."]


@pytest.mark.django_db
def test_register_view_with_unique_emails(user, anonymous_client):
    """Test that it raises error when entered email is not unique """
    url = reverse("register")

    data={
        "email":'test@gmail.com',
        "fullname": 'test3',
        "password1": "1234",
        "password2": "1234"
    }

    res = anonymous_client.post(url, data=data,format='json')

    assert not res.status_code == status.HTTP_201_CREATED
    assert res.data['email'] == ['User with this email address already exists.']
        


 