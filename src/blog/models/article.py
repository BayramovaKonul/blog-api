from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from ckeditor.fields import RichTextField
from .category import CategoryModel
from .abstract_model import CreationDateAbstractModel

User = get_user_model()

class ArticleModel(CreationDateAbstractModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, 
                                  related_name="articles", verbose_name=_("author"))
    title = models.CharField(verbose_name=_("title"), max_length=255)
    slug = AutoSlugField(populate_from="title", unique=True)
    content = RichTextField(verbose_name=_("content"))
    published_at = models.DateTimeField(verbose_name=_("published_at"), null=True, blank=True)
    picture = models.ImageField(verbose_name=_("picture"), upload_to='media/article_images/')
    categories = models.ManyToManyField(CategoryModel, related_name="articles", verbose_name=_("categories"))

    class Meta:
        db_table = 'article'
        verbose_name = _('Article')
        verbose_name_plural = _("Articles")

    def __str__(self):
        return f"{self.title}, {self.author.fullname}"