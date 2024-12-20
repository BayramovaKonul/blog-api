# code
from django.db.models.signals import post_save, pre_delete

from django.dispatch import receiver
from .models import UserProfile, CustomUser
 
 
@receiver(post_save, sender=CustomUser) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        # create profile table when user is created
  
@receiver(post_save, sender=CustomUser) 
def save_profile(sender, instance, **kwargs):
        instance.profile.save()
        #update profile table when user is updated