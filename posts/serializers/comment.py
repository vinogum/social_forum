from rest_framework.serializers import ModelSerializer
from posts.models import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "post", "user", "text", "created_at")
        read_only_fields = ("user", "post", "created_at")
