from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ArticleBaseSerializer, ArticleDetailSerializer, ArticlesCommentSerializer
from .models import ArticleModel, CommentModel
from django.shortcuts import get_object_or_404
from django.db.models import Count

class ArticleBaseView(APIView):
    def get(self, request):
        articles=ArticleModel.objects.all()
        serializers=ArticleBaseSerializer(articles, many=True)
        return Response(
            data=serializers.data,
            status=status.HTTP_200_OK)
   
class ArticleDetailView(APIView):
    def get(self, request, slug):
        article = get_object_or_404(ArticleModel, slug=slug)
        serializer=ArticleDetailSerializer(article)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK)
    
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
    