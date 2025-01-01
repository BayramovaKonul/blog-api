from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User= get_user_model()

class UserFollowerModel(models.Model):
    follower=models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="followers", verbose_name=_("follower"))
    following=models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="followings", verbose_name=_("following"))
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table='user_follower'
        verbose_name=_('User_follower')
        verbose_name_plural=_('User_followers')

    def __str__(self):
        return f"{self.follower}->{self.following}"