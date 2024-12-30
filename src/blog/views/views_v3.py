from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import ArticleModel
from account.models import CustomUser
from ..serializers import ArticleDetailSerializer, ArticleUpdateSerializer, ArticleWriteSerializer, ArticleReadSerializer
from rest_framework.exceptions import NotFound

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = ArticleModel.objects.all()
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleDetailSerializer  # get/detail
        elif self.action in ['update', 'partial_update']:
            return ArticleUpdateSerializer # put or patch
        elif self.action == 'list':
            return ArticleReadSerializer  # get all articles
        return ArticleWriteSerializer # post

    def perform_create(self, serializer):
        request_user = CustomUser.objects.get(id=1)
        serializer.save(author=request_user)
    

    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        article.delete()
        return Response(
            data={"success": "Article successfully deleted."},
            status=status.HTTP_204_NO_CONTENT
        )
