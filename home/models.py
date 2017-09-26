from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    file = models.ImageField(upload_to='profile_image/', blank=True, default='profile_image/no_profile.jpg', verbose_name=_('File'))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_('Birth date'))

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
