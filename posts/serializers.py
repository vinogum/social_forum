from rest_framework import serializers
from .models import Post


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]
        extra_kwargs = {
            "image": {
                "write_only": True,
                "required": False,
            }
        }

    def validate(self, attrs):
        title = attrs.get("title")
        text = attrs.get("text")
        if not isinstance(title, str) or len(title) == 0:
            raise serializers.ValidationError("Invalid title!")
        if not isinstance(text, str) or len(text) == 0:
            raise serializers.ValidationError("Invalid text!")
        return attrs
    
    def validate_image(self, image):
        if not hasattr(image, "size"):
            raise serializers.ValidationError("Image is required!")
        if image.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image size must be at most 2MB!")
        
        if not image.content_type.startswith('image/'):
            raise serializers.ValidationError("Support only image files!")
        
        return image


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "user", "title", "text", "created_at"]
        read_only_fields = ["id", "user", "title", "text", "created_at"]
