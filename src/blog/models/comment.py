from django.db import models
from django.contrib.auth import get_user_model
from .article import ArticleModel
from django.utils.translation import gettext as _

User = get_user_model()

class CommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="comments", verbose_name=_("user"))
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE,
                                related_name="comments", verbose_name=_("article"))
    content = models.TextField(verbose_name=_("content"))
    created_at = models.DateTimeField(verbose_name=_("created_at"), auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                               related_name="replies", verbose_name=_("parent comment"))


    class Meta:
        db_table = 'comment'
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


    def __str__(self):
        return f"{self.article}, {self.user.fullname}"