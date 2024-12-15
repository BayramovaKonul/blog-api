from django.contrib import admin

from .models import CategoryModel, ArticleModel, CommentModel, ContactUsModel

@admin.register(ArticleModel)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'published_at'] 
    list_display_links = ['title', 'created_at'] 
    search_fields = ['title', 'content'] 
    list_filter = ['created_at']

@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name'] 
    list_display_links = ['name'] 
    search_fields = ['name']


@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'article', 'user', 'created_at'] 
    list_display_links = ['user', 'article']
    search_fields = ['content'] 
    list_filter = ['created_at']

@admin.register(ContactUsModel)
class CommentUsAdmin(admin.ModelAdmin):
    list_display = ['subject', 'message','created_at'] 
    list_display_links = ['subject', 'message'] 
    search_fields = ['subject'] 
    list_filter = ['created_at']