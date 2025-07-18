from rest_framework import serializers
from .models import Post, Image, Comment, Reaction, ReactionType
from .utilities import get_file_hash
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
    type_display = serializers.CharField(source="get_type_display", read_only=True)

    class Meta:
        model = Reaction
        fields = ("user", "post", "type", "type_display")
        read_only_fields = ("user", "post", "type_display")

    def validate(self, attrs):
        type = attrs.get("type")

        if type not in ReactionType.values:
            raise serializers.ValidationError("Invalid reaction type")

        return attrs

    def create(self, validated_data):
        user = validated_data.get("user")
        post = validated_data.get("post")

        if not user or not post:
            raise serializers.ValidationError("User or Post data is missing")

        reaction, created = Reaction.objects.update_or_create(
            user=user, post=post, defaults={"type": validated_data["type"]}
        )
        return reaction


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "text")
