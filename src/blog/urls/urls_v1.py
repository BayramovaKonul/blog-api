"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ..views import views_v1
from ..views.views_v1 import ArticleBaseView, ArticleDetailView, MainCommentView, BookMarkView, ContactUsView, MyArticlesView, AllCommentsView

urlpatterns = [
    path(_("articles"), views_v1.ArticleBaseView.as_view(), name="articles"),
    path(_("articles/<slug:slug>/"), views_v1.ArticleDetailView.as_view(), name="article/detail"),
    path(_("articles/<slug:slug>/comments"), views_v1.MainCommentView.as_view(), name="main_comments"),
    path(_("comments/<int:id>/replies"), views_v1.AllCommentsView.as_view(), name="all_comments"),
    path(_("articles/<slug:slug>/comments/<int:comment_id>/"), views_v1.MainCommentView.as_view(), name="delete_update_comment"),
    path(_("bookmarks/<int:article_id>/"), views_v1.BookMarkView.as_view(), name="create_bookmark"),
    path(_("bookmarks/"), views_v1.BookMarkView.as_view(), name="bookmarks"),
    # path(_("category/"), views_v1.CategoryView.as_view(), name="add_category"),
    # path(_("category/<int:id>/"), views_v1.CategoryView.as_view(), name="delete_category"),
    # path(_("categories/"), views_v1.CategoryView.as_view(), name="categories"),
    path(_("contactus/"), views_v1.ContactUsView.as_view(), name="contact_us"),
     path(_("myarticles/"), views_v1.MyArticlesView.as_view(), name="ay_articles"),
]
