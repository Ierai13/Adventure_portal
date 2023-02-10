from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Reply
from .tasks import new_reply


@receiver(post_save, sender=Reply)
def notify_author(sender, instance, **kwargs):
    if kwargs['created']:
        new_reply(instance)