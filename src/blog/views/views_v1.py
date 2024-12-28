from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import (ArticleReadSerializer, ArticleDetailSerializer, 
                          ArticlesCommentSerializer, ArticleWriteSerializer, ArticleUpdateSerializer, 
                          AllCommentSerializer, BookMarkSerializer, CategoryReadSerializer, ContactUsSerializer)
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
        
        
    def validate_picture(self, value):
        # Guess the MIME type of the uploaded file based on its extension
        mime_type, encoding = mimetypes.guess_type(value.name)
        
        # Allowed image MIME types
        valid_mime_types = ['image/jpeg', 'image/png']
        
        # Check if the file's MIME type is in the allowed list
        if mime_type not in valid_mime_types:
            raise ValidationError(f"Only image files are allowed. Detected file type: {mime_type}")
        
        return value
        
   
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
    def get(self, request, slug, id):
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
    def post(self, request):
        
        article_id = request.data.get('article_id')  

        if not article_id:
            return Response({"detail": "No article."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the article from the database using the ID
        article = get_object_or_404(ArticleModel, id=article_id)
        request_user = CustomUser.objects.get(id=1)

        # Check if the user has already bookmarked this article
        if BookMarkModel.objects.filter(user=request_user, article=article).exists():
            return Response({"detail": "You have already bookmarked this article."}, status=status.HTTP_400_BAD_REQUEST)
        
        bookmark = BookMarkModel.objects.create(user=request_user, article=article)
        serializer = BookMarkSerializer(bookmark)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    def delete(self, request):
        article_id = request.data.get('article_id')
        article = get_object_or_404(BookMarkModel, id=article_id)
        article.delete()
        return Response(
            data={"success": True},
            status=status.HTTP_204_NO_CONTENT
        )
    
class CategoryView (APIView):
    def post(self, request):
        name = request.data.get('name')

        if CategoryModel.objects.filter(name=name):
            return Response({"detail": "This category has been added before"}, status=status.HTTP_400_BAD_REQUEST)            

        serializer = CategoryReadSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                    )
        
    def delete(self, request):
        slug = request.data.get('slug')
        category = get_object_or_404(CategoryModel, slug=slug)
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
    

