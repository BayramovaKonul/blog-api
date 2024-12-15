from django.db import models
from django.contrib.auth import get_user_model
from .article import ArticleModel
from django.utils.translation import gettext as _
from .abstract_model import CreationDateAbstractModel

User = get_user_model()

class BookMarkModel(CreationDateAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="bookmark", verbose_name=_("user"))
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE,
                                related_name="bookmarked_articles", verbose_name=_("article"))
  

    class Meta:
        db_table = 'bookmark'
        verbose_name = _('Bookmark')
        verbose_name_plural = _('Bookmarks')


    def __str__(self):
        return f"{self.user.fullname}, {self.article.title}"