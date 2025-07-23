from rest_framework import serializers
from posts.models import Post, Image, Comment, Reaction
from posts.utilities import get_file_hash
from social_forum import settings


class ImageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("post", "image_data", "image_hash")
        read_only_fields = ("post", "image_hash")

    def validate(self, attrs):
        image = attrs.get("image_data")
        if not image:
            raise serializers.ValidationError("Image not found")

        if not image.content_type.startswith("image/"):
            raise serializers.ValidationError("Support only image files")

        if image.size > settings.MAX_IMAGE_SIZE_BYTES:
            raise serializers.ValidationError(
                f"Image size must be at most {settings.MAX_IMAGE_SIZE_BYTES}MB"
            )

        try:
            image_hash = get_file_hash(image)
        except TypeError as e:
            raise serializers.ValidationError(f"Failed to get the file hash: {e}")

        attrs["image_hash"] = image_hash
        return attrs


class ImageReadSerializer(serializers.Serializer):
    image_data = serializers.CharField(read_only=True)


class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("id", "user", "created_at")


class PostReadSerializer(serializers.ModelSerializer):
    images = ImageReadSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ("id", "user", "title", "text", "images", "created_at")
        read_only_fields = fields


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "post", "user", "text", "created_at")
        read_only_fields = ("user", "post", "created_at")


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ("id", "user", "post", "type")
        read_only_fields = ("id", "user", "post")


class ReactionCreateSerializer(serializers.ModelSerializer):
    class Meta(ReactionSerializer.Meta):
        pass

    def validate(self, attrs):
        request = self.context.get("request")
        post_pk = self.context.get("post_pk")

        if not request or not post_pk:
            raise serializers.ValidationError("The variables request and post_pk are required")

        if Reaction.objects.filter(user=request.user, post=post_pk).exists():
            raise serializers.ValidationError(f"Reaction already exists from user with ID {request.user.id}")
        
        return attrs


class ReactionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ("id", "post", "user", "type")
        read_only_fields = fields


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "text")
        extra_kwargs = {
            "title": {"required": False},
            "text": {"required": False},
        }
