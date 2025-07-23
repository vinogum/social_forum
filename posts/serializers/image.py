from rest_framework import serializers
from posts.models import Image
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
