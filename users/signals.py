from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile_with_new_user(sender, instance, created, raw, **kwargs):
    if created and not raw:
        profile = Profile.objects.create(user=instance)
        instance.profile = profile
        instance.save()
