from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User= get_user_model()

class UserProfile(models.Model):
    birthday=models.DateTimeField(verbose_name=_("birthday"), null=True, blank=True)
    profile_pic=models.ImageField(verbose_name=_("profile_pic"), upload_to='media/user_profile_pictures/', blank = True, null= True)
    user=models.OneToOneField(User, on_delete=models.CASCADE,
                             related_name="profile", verbose_name=_("user"))

    class Meta:
        db_table='user_profile'
        verbose_name=_('User_profile')
        verbose_name_plural=_('User_profiles')

    def __str__(self):
        return f"{self.user.username}"