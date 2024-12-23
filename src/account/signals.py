# code
from django.db.models.signals import post_save, pre_delete

from django.dispatch import receiver
from .models import UserProfile, CustomUser
 
 
@receiver(post_save, sender=CustomUser) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
