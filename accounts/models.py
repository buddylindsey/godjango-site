import arrow

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField('auth.User')
    last_access = models.DateTimeField(blank=True, null=True)

    def update_last_access(self):
        now = arrow.utcnow().datetime
        #check_for_new_videos.delay(last_access, now)
        self.last_access = now
        self.save(update_fields=['last_access'])


@receiver(post_save, sender=User)
def distance_settings(sender, **kwargs):
    user = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        Profile.objects.create(user=user)
