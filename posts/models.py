from django.db import models
from .utilities import upload_to
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    created_at = models.DataTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Reaction(models.Model):
    LIKE = 1
    DISLIKE = -1
    NONE = 0

    REACTION_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
        (NONE, "None"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reactions")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    reaction = models.IntegerField(choices=REACTION_CHOICES, default=NONE)
