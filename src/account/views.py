from django.shortcuts import render
from .serializers import UserReadSerializer, UserProfileSerializer
from .models import CustomUser, UserProfile
from django.http import HttpResponse
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

class UpdateUserProfile(APIView):
    def patch(self, request):
        # Hardcoded user for testing
        request_user = CustomUser.objects.get(id=1)
        user_profile = request_user.profile # profile is a related name
        # Initialize the serializer
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
