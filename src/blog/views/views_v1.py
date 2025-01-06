from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import (ArticleReadSerializer, ArticleDetailSerializer, 
                          ArticlesCommentSerializer, ArticleWriteSerializer, ArticleUpdateSerializer, 
                          AllCommentSerializer, BookMarkWriteSerializer, CategoryReadSerializer,BookMarkReadSerializer, 
                          CategoryWriteSerializer, ContactUsSerializer, UpdateCommentSerializer)
from ..models import ArticleModel, CommentModel, BookMarkModel, CategoryModel
from django.shortcuts import get_object_or_404
from django.db.models import Count
from ..pagination import MyPagination
from account.models import CustomUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q, Prefetch
import mimetypes
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from ..custom_permissions import IsArticleAuthorOrReadOnly, IsCommentAuthorOrReadOnly
from drf_yasg import openapi

class ArticleBaseView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes=[IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "follower_fullname",
                openapi.IN_QUERY,
                description="Filter followers by full name (case-insensitive match).",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Specify the page number for pagination.",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: openapi.Response(
                description="A list of followers.",
                schema=ArticleReadSerializer(many=True),
            ),
            400: "Bad Request",
        }
    )
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

        paginator = MyPagination()
        paginated_articles = paginator.paginate_queryset(articles, request)
        serializers=ArticleReadSerializer(paginated_articles, many=True)
        return paginator.get_paginated_response(serializers.data)
    

    @swagger_auto_schema(
    request_body=ArticleWriteSerializer,
    responses={201: ArticleReadSerializer()})
    def post(self, request):
        serializer = ArticleWriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED)
     
        
   
class ArticleDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsArticleAuthorOrReadOnly] 
    def get_object(self, slug):
        return get_object_or_404(ArticleModel, slug=slug)

    @swagger_auto_schema(responses={200: ArticleDetailSerializer()})
    def get(self, request, slug):
        article = self.get_object(slug)
        serializer = ArticleDetailSerializer(article)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, slug):
        article = self.get_object(slug)
        self.check_object_permissions(request, article) # explicitly called
        article.delete()
        return Response(
            data={"success": True},
            status=status.HTTP_204_NO_CONTENT
        )
    @swagger_auto_schema(
        request_body=ArticleUpdateSerializer,
        responses={200: ArticleReadSerializer()})
    
    def patch(self, request, slug):
        article = self.get_object(slug)
        print(f"Request user: {request.user}, Article author: {article.author}") 
        self.check_object_permissions(request, article) # explicitly called
        serializer = ArticleUpdateSerializer(data=request.data, instance=article, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                    )
        
    @swagger_auto_schema(
        request_body=ArticleUpdateSerializer,
        responses={200: ArticleReadSerializer()})
    
    def put(self, request, slug):
        article = self.get_object(slug)
        self.check_object_permissions(request, article) # explicitly called
        serializer = ArticleUpdateSerializer(data=request.data, instance=article)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                    )

@swagger_auto_schema(responses={200: ArticlesCommentSerializer(many=True)})    
class MainCommentView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly, IsCommentAuthorOrReadOnly]

    @swagger_auto_schema(responses={200: ArticlesCommentSerializer(many=True)})
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
    
    def get_article_comment(self, slug, comment_id):
        article = get_object_or_404(ArticleModel, slug=slug)
        comment = article.comments.get(id=comment_id)
        return article, comment


    @swagger_auto_schema(
        responses={
            204: 'Comment was deleted successfully',
        }
    )
    def delete(self, request, slug, comment_id):
        # ignore article (return value of the helper method) by using _
        _, comment = self.get_article_comment(slug, comment_id)
        self.check_object_permissions(request, comment) # explicitly called
        # Delete the comment
        comment.delete()
        return Response(
                data={"success": True},
                status=status.HTTP_204_NO_CONTENT)
    

    @swagger_auto_schema(
        request_body=UpdateCommentSerializer,
        responses={
            200: UpdateCommentSerializer,
            400: 'Bad request, invalid data.',
        }
    )
    def put(self, request, slug, comment_id):
        _, comment = self.get_article_comment(slug, comment_id)
        self.check_object_permissions(request, comment) # explicitly called
        serializer=UpdateCommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK)
       

@swagger_auto_schema(responses={200: AllCommentSerializer(many=True)})    
class AllCommentsView(APIView):
    def get(self, request, id):
        # Retrieve the comment by its ID
        comment = get_object_or_404(CommentModel, id=id)

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
        # Check if the user has already bookmarked this article
        if BookMarkModel.objects.filter(user=request.user, article__id=article_id).exists():
            return Response({"detail": "You have already bookmarked this article."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BookMarkWriteSerializer(data={"article": article_id})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
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

    def get(self, request):
        article_slug = request.query_params.get('article_slug')
        user= request.user
        bookmarks=BookMarkModel.objects.filter(user=user)

        if article_slug:
            bookmarks = bookmarks.filter(article__slug__icontains=article_slug)

        paginator = MyPagination()
        paginated_bookmarks=paginator.paginate_queryset(bookmarks, request) 
        serializer=BookMarkReadSerializer(paginated_bookmarks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
# class CategoryView (APIView):
#     def post(self, request):
#         serializer = CategoryWriteSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(
#                     data=serializer.data,
#                     status=status.HTTP_201_CREATED
#                     )
        
#     def delete(self, request, id):
#         category = get_object_or_404(CategoryModel, id=id)
#         category.delete()
#         return Response(
#             data={"success": True},
#             status=status.HTTP_204_NO_CONTENT
#         )
    
#     def get(self, request):
#         categories=CategoryModel.objects.all()
#         category_slug = request.query_params.get('category_slug')
        
#         if category_slug:
#             categories = categories.filter(slug__icontains=category_slug)

#         paginator = MyPagination()
#         paginated_categories=paginator.paginate_queryset(categories, request) 
#         serializer=CategoryReadSerializer(paginated_categories, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class ContactUsView(APIView):
    @swagger_auto_schema(
    request_body=ContactUsSerializer,
    responses={
        201: ContactUsSerializer,  # This will show the serializer data as response
        400: 'Bad request, invalid input data.'
    }
)
    def post (self, request):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED)


class MyArticlesView(APIView):
    def get(self, request):
        my_articles= ArticleModel.objects.filter(author=request.user)
        serializer = ArticleReadSerializer(my_articles, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    

