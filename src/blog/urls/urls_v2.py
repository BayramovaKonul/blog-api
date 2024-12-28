from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ..views import views_v2
from ..views.views_v2 import (ArticleListView, CreateArticleView, ArticleDeleteAPIView, 
                              ArticleUpdateAPIView, ArticleDetailAPIView, MyArticlesListView)

urlpatterns = [
    path("articles/", views_v2.ArticleListView.as_view(), name="articles"),
    path("myarticles/", views_v2.MyArticlesListView.as_view(), name="my_articles"),
    path("create/article", views_v2.CreateArticleView.as_view(), name="create_article"),
    path("delete/article/<slug:slug>/", views_v2.ArticleDeleteAPIView.as_view(), name="delete_article"),
    path("update/article/<slug:slug>/", views_v2.ArticleUpdateAPIView.as_view(), name="update_article"),
    path("articles/<slug:slug>/", views_v2.ArticleDetailAPIView.as_view(), name="article_detail"),
]
