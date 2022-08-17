from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from ..users.models import Profile
from .models import Order,rregister
@receiver(post_save, sender=rregister)
def create_order(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=rregister)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()        