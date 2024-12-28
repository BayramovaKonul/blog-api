from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import (ArticleReadSerializer, ArticleDetailSerializer, 
                          ArticlesCommentSerializer, ArticleWriteSerializer, ArticleUpdateSerializer, 
                          AllCommentSerializer, BookMarkSerializer, CategoryReadSerializer, ContactUsSerializer)
from ..models import ArticleModel, CommentModel, BookMarkModel, CategoryModel
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from ..pagination import ArticlePagination
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from account.models import CustomUser
from datetime import datetime

class ArticleListView(generics.ListAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleReadSerializer
    pagination_class = ArticlePagination

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(published_at__gte=datetime.now())
        query_params = dict(self.request.query_params)
        search=query_params.get('search')  # get search from the request
        if search:
            queryset = queryset.filter(Q(title__icontains=search[0]) |
                                       Q(content__icontains=search[0]))
        return queryset
    
class MyArticlesListView(generics.ListAPIView):
    serializer_class = ArticleReadSerializer
    pagination_class = ArticlePagination

    def get_queryset(self):
        user = CustomUser.objects.get(id=1)
        return ArticleModel.objects.filter(author=user)


class CreateArticleView(generics.CreateAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleWriteSerializer
    
    # perform_create is called after serializer validate data and it fills the part which setting default values or assigning related fields that are not included in the incoming data
    def perform_create(self, serializer):
        request_user = CustomUser.objects.get(id=1)
        serializer.save(author=request_user)


class ArticleDeleteAPIView(generics.DestroyAPIView):
    queryset = ArticleModel.objects.all()

    def get_object(self):
        # fetch article based on its slug and delete
        slug = self.kwargs['slug']
        return ArticleModel.objects.get(slug=slug)


class ArticleUpdateAPIView(generics.UpdateAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleUpdateSerializer
    lookup_field = 'slug'  # Use 'slug' as the identifier for lookup

    def update(self, request, *args, **kwargs):
        # This is the default method for handling both PUT and PATCH requests.

        response = super().update(request, *args, **kwargs)
        return Response(
            data=response.data,
            status=status.HTTP_200_OK
        )

class ArticleDetailAPIView(generics.RetrieveAPIView):
    queryset = ArticleModel.objects.all()  # The queryset to filter objects
    serializer_class = ArticleDetailSerializer  # The serializer for formatting the response
    lookup_field = 'slug'  # Use 'slug' as the identifier
