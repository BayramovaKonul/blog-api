from django.shortcuts import render
from .serializers import UserReadSerializer, UserProfileSerializer
from .models import CustomUser, UserProfile
from django.http import HttpResponse
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

def home(request):
    return HttpResponse("Hello, World!")


class UpdateUserProfile(APIView):
    def patch(self, request):
        # Hardcoded user for testing
        request_user = CustomUser.objects.get(id=3)

        # Get the UserProfile instance or raise a 404 error if it does not exist
        user_profile = get_object_or_404(UserProfile, )

        # Initialize the serializer
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)
            
