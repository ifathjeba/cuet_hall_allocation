from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        # New users default to 'student' (signup will override if necessary)
        Profile.objects.create(user=instance, user_type='student')
    else:
        # Ensure a profile exists for existing users
        Profile.objects.get_or_create(user=instance)