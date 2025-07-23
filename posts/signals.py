from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Post
import logging

logger = logging.getLogger("django")


@receiver(post_save, sender=Post)
def log_post_creation(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Post was created by user {instance.user_id}")
