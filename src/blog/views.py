from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (ArticleReadSerializer, ArticleDetailSerializer, 
                          ArticlesCommentSerializer, ArticleWriteSerializer, ArticleUpdateSerializer)
from .models import ArticleModel, CommentModel
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .pagination import ArticlePagination
from account.models import CustomUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ArticleBaseView(APIView):
    def get(self, request):
        query_params = dict(request.query_params)
        title = query_params.get('title')  # get title from request for filtering
        categories = query_params.get('ctg')
        articles=ArticleModel.objects.all().prefetch_related('categories').select_related('author')

        if title:
            articles = articles.filter(title__icontains=title[0])
        if categories:
            categories=[int(i) for i in categories]
            articles = articles.filter(categories__id__in=categories)

        paginator = ArticlePagination()
        paginated_articles = paginator.paginate_queryset(articles, request)
        serializers=ArticleReadSerializer(paginated_articles, many=True)
        return paginator.get_paginated_response(serializers.data)
    
    def post(self, request):
        request_user = CustomUser.objects.get(id=1)
        serializer = ArticleWriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request_user)
            return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED)
        
   
class ArticleDetailView(APIView):

    def get_object(self, slug):
        return get_object_or_404(ArticleModel, slug=slug)

    def get(self, request, slug):
        article = self.get_object(slug)
        serializer = ArticleDetailSerializer(article)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, slug):
        # permission_classes = [IsAuthenticatedOrReadOnly]
        article = self.get_object(slug)
        article.delete()
        return Response(
            data={"success": True},
            status=status.HTTP_204_NO_CONTENT
        )
    
    def patch(self, request, slug):
        article = self.get_object(slug)
        serializer = ArticleUpdateSerializer(data=request.data, instance=article, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                    )

    def put(self, request, slug):
        article = self.get_object(slug)
        serializer = ArticleUpdateSerializer(data=request.data, instance=article)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                    )

    
class AllCommentView(APIView):
    def get(self, request):
        # Query all articles with their related comments
        articles = ArticleModel.objects.prefetch_related('comments').annotate(comment_count=Count('comments'))  # 'comments' is the related_name for CommentModel
        serializer = ArticlesCommentSerializer(articles, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    
class ArticleCommentView(APIView):
    def get(self, request, id):
        article_comment=get_object_or_404(ArticleModel.objects.prefetch_related('comments')
                                          .annotate(comment_count=Count('comments')), id=id)
        serializer=ArticlesCommentSerializer(article_comment)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
            )
    