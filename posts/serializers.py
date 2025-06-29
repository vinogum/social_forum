from rest_framework import serializers
from .models import Post, Image, Comment
from .utilities import get_file_hash


class ImageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("post", "image_data", "image_hash")
        read_only_fields = ("post", "image_hash")

    def validate(self, attrs):
        MAX_IMAGE_SIZE_BYTES = 2 * 1024 * 1024

        image = attrs.get("image_data")
        if not image:
            raise serializers.ValidationError("Image not found!")

        if not image.content_type.startswith("image/"):
            raise serializers.ValidationError("Support only image files!")

        if image.size > MAX_IMAGE_SIZE_BYTES:
            raise serializers.ValidationError(
                f"Image size must be at most {MAX_IMAGE_SIZE_BYTES}MB!"
            )

        image_hash = get_file_hash(image)
        if image_hash is None:
            raise serializers.ValidationError("Failed to get the file hash!")

        attrs["image_hash"] = image_hash
        return attrs


class ImageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("image_data",)
        read_only_fields = ("image_data",)


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
