from posts.serializers import comment, image
from rest_framework.serializers import ModelSerializer
from posts.models import Post


class PostWriteSerializer(ModelSerializer):
    images = image.ImageReadSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ("id", "user", "title", "text", "images", "created_at")
        read_only_fields = ("id", "user", "images", "created_at")


class PostReadSerializer(ModelSerializer):
    images = image.ImageReadSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ("id", "user", "title", "text", "images", "created_at")
        read_only_fields = fields


class PostRetrieveSerializer(ModelSerializer):
    images = image.ImageReadSerializer(many=True, required=False)
    comments = comment.CommentSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ("id", "user", "title", "text", "images", "comments", "created_at")
        read_only_fields = fields


class PostUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "text")
        extra_kwargs = {
            "title": {"required": False},
            "text": {"required": False},
        }
