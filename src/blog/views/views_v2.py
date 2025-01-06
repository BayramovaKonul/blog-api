from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import (ArticleReadSerializer, ArticleDetailSerializer, 
                          ArticlesCommentSerializer, ArticleWriteSerializer, ArticleUpdateSerializer, 
                          AllCommentSerializer, BookMarkWriteSerializer, CategoryReadSerializer, ContactUsSerializer)
from ..models import ArticleModel, CommentModel, BookMarkModel, CategoryModel
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from ..pagination import MyPagination
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from account.models import CustomUser
from datetime import datetime

class ArticleListCreateView(generics.ListCreateAPIView):
    serializer_class = ArticleReadSerializer  # Use read serializer for listing
    pagination_class = MyPagination

    def get_queryset(self):
        # List all articles published from the current time 
        queryset = ArticleModel.objects.filter(published_at__gte=datetime.now())
        search = self.request.query_params.get('search')  # Get 'search' query param
        if search:
            queryset = queryset.filter(Q(title__icontains=search[0]) | Q(content__icontains=search[0]))
        return queryset

    def get_serializer_class(self):
        # Use different serializers for GET and POST methods
        if self.request.method == 'POST':
            return ArticleWriteSerializer 
        return ArticleReadSerializer

    def perform_create(self, serializer):
        # Automatically set the authenticated user as the author
        request_user = CustomUser.objects.get(id=1)
        serializer.save(author=self.request.user)

    
class MyArticlesListView(generics.ListAPIView):
    serializer_class = ArticleReadSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        user = CustomUser.objects.get(id=1)
        return ArticleModel.objects.filter(author=user)

class ArticleDeleteAPIView(generics.DestroyAPIView):
    queryset = ArticleModel.objects.all()

    def get_object(self):
        # fetch article based on its slug and delete
        slug = self.kwargs['slug']
        return ArticleModel.objects.get(slug=slug)


class ArticleRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = ArticleModel.objects.all()
    lookup_field = 'slug'  # Use 'slug' as the identifier for lookup

    def get_serializer_class(self):
        # Return the appropriate serializer based on the request method
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return ArticleUpdateSerializer
        return ArticleDetailSerializer

    def update(self, request, *args, **kwargs):
        # This is the default method for handling both PUT and PATCH requests.
        response = super().update(request, *args, **kwargs)
        return Response(
            data=response.data,
            status=status.HTTP_200_OK
        )
