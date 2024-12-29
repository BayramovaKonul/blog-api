from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import (ArticleReadSerializer, ArticleDetailSerializer, 
                          ArticlesCommentSerializer, ArticleWriteSerializer, ArticleUpdateSerializer, 
                          AllCommentSerializer, BookMarkSerializer, CategoryReadSerializer, CategoryWriteSerializer, ContactUsSerializer)
from ..models import ArticleModel, CommentModel, BookMarkModel, CategoryModel
from django.shortcuts import get_object_or_404
from django.db.models import Count
from ..pagination import ArticlePagination
from account.models import CustomUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q, Prefetch
import mimetypes
from django.core.exceptions import ValidationError

class ArticleBaseView(APIView):
    def get(self, request):
        query_params = dict(request.query_params)
        search=query_params.get('search')  # get search from the request
        categories = query_params.get('ctg')
        articles=ArticleModel.objects.all().prefetch_related('categories').select_related('author')
        
        if search:
            articles = articles.filter(Q(title__icontains=search[0]) |
                                       Q(content__icontains=search[0]))
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

    
class MainCommentView(APIView):
    def get(self, request, slug):
        # Prefetch only the main comments (no parent)
        main_comments = Prefetch('comments', queryset=CommentModel.objects.filter(parent__isnull=True))

        # Retrieve the article with the prefetch of main comments and annotate comment count
        article = get_object_or_404(
                    ArticleModel.objects.prefetch_related(main_comments).annotate(
                    comment_count=Count('comments', filter=Q(comments__parent__isnull=True))
                    ),slug=slug)
        
        # Serialize the article with its main comments and comment count
        serializer = ArticlesCommentSerializer(article)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    
class AllCommentsView(APIView):
    def get(self, request, id):
        # Retrieve the comment by its ID
        comment = get_object_or_404(CommentModel, id=id)

        print("comment", comment)
        # Retrieve all replies to the comment 
        replies = CommentModel.objects.filter(parent=comment)

        # Serialize the replies
        serializer = AllCommentSerializer(replies, many=True)

        # Return the serialized data
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    

class BookMarkView(APIView):
    def post(self, request, article_id):
        request_user = CustomUser.objects.get(id=1)

        # Check if the user has already bookmarked this article
        if BookMarkModel.objects.filter(user=request_user, article__id=article_id).exists():
            return Response({"detail": "You have already bookmarked this article."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BookMarkSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request_user, article_id=article_id)
            return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED)
    
    
    def delete(self, request, article_id):
        article = get_object_or_404(BookMarkModel, article_id=article_id)
        article.delete()
        return Response(
            data={"success": True},
            status=status.HTTP_204_NO_CONTENT
        )
    
class CategoryView (APIView):
    def post(self, request):
        serializer = CategoryWriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                    )
        
    def delete(self, request, id):
        category = get_object_or_404(CategoryModel, id=id)
        category.delete()
        return Response(
            data={"success": True},
            status=status.HTTP_204_NO_CONTENT
        )

class ContactUsView(APIView):
    def post (self, request):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED)


class MyArticlesView(APIView):
    def get(self, request):
        request_user = CustomUser.objects.get(id=1)
        my_articles= ArticleModel.objects.filter(author=request_user)
        serializer = ArticleReadSerializer(my_articles, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    

