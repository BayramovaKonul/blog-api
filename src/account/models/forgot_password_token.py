from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import uuid

User= get_user_model()

def get_expiry_date():
    return timezone.now() + timedelta(days=1)

class ForgotPasswordTokenModel(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="forgot_password_tokens", verbose_name=_("user"))
    
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(default=get_expiry_date)
    # add is_used field here as the default value is false
    class Meta:
        db_table='forgot_password_token'
        verbose_name=_('Forgot_password_token')
        verbose_name_plural=_('Forgot_password_tokens')

    def __str__(self):
        return f"{self.user.fullname} -> {self.created_at}"
    

    def is_expired(self):
        #Check if the token is expired
        return timezone.now() > self.expired_at