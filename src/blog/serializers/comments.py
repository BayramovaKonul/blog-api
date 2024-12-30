from rest_framework import serializers
from ..models import ArticleModel, CommentModel
from rest_framework.fields import SerializerMethodField

class AllCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['user', 'content', 'parent']

class ArticlesCommentSerializer(serializers.ModelSerializer):
    comments = AllCommentSerializer(many=True, read_only=True) 
    comment_count = SerializerMethodField()  # Custom field to get the comment count
    class Meta:
        model = ArticleModel
        fields = ['title', 'author', 'created_at', 'comment_count', 'comments']  

    def get_comment_count(self, obj):
        # Count the number of main comments (parent is null)
        return obj.comments.filter(parent__isnull=True).count()