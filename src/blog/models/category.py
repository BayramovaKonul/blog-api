from django.db import models
from autoslug import AutoSlugField
from django.utils.translation import gettext as _

class CategoryModel(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=100, null=False, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True)

    class Meta:
        db_table = 'category'
        verbose_name = _('Category')
        verbose_name_plural = _("Categories")
        
    def __str__(self):
        return f"{self.name}"