from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ..views import views_v2
from ..views.views_v2 import (ArticleListCreateView, ArticleDeleteAPIView, 
                              ArticleRetrieveUpdateAPIView, MyArticlesListView)

urlpatterns = [
    path("articles/", views_v2.ArticleListCreateView.as_view(), name="list_create_article"),
    path("myarticles/", views_v2.MyArticlesListView.as_view(), name="my_articles"),
    path("delete/article/<slug:slug>/", views_v2.ArticleDeleteAPIView.as_view(), name="delete_article"),
    path("articles/<slug:slug>/", views_v2.ArticleRetrieveUpdateAPIView.as_view(), name="retrieve_update"),
]
