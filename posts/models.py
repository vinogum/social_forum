from django.db import models
from .utilities import upload_to
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image_data = models.ImageField(upload_to=upload_to, null=True, blank=True)
    image_hash = models.CharField(max_length=128)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class ReactionType(models.IntegerChoices):
    NONE = 0, "None"
    DISLIKE = -1, "Dislike"
    LIKE = 1, "Like"


class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reactions")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    type = models.IntegerField(choices=ReactionType.choices, default=ReactionType.NONE)

    class Meta:
        unique_together = ("user", "post")
