from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if not isinstance(username, str) or len(username) == 0:
            raise serializers.ValidationError("Invalid username!")

        if not isinstance(password, str) or len(password) == 0:
            raise serializers.ValidationError("Invalid password!")

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )
        return user
