from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from .abstract_model import CreationDateAbstractModel

User = get_user_model()

class ContactUsModel(CreationDateAbstractModel):
    class StageChoices(models.TextChoices):
        NEW = 'new', 'New'
        IN_REVIEW = 'in_review', 'In Review'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'
        CLOSED = 'closed', 'Closed'


    email = models.EmailField(verbose_name=_("email"), null = False)
    subject = models.CharField(verbose_name=_("subject"), max_length=200)
    message = models.TextField(verbose_name=_("message"))
    stage = models.CharField(verbose_name=_("stage"), max_length=20, choices=StageChoices.choices, default=StageChoices.NEW)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank=True,
                             related_name="assigned", verbose_name=_("assigned_to"))
    resolved_at = models.DateTimeField(verbose_name=_("resolved_at"), null = True, blank = True)
    
    class Meta:
        db_table = 'user_messages'
        verbose_name = _('ContactUs')
        verbose_name_plural = _("ContactUs")
        
    def __str__(self):
        return f"{self.subject}"