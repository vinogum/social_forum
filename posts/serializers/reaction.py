from rest_framework.serializers import ModelSerializer, ValidationError
from posts.models import Reaction


class ReactionSerializer(ModelSerializer):
    class Meta:
        model = Reaction
        fields = ("id", "user", "post", "type")
        read_only_fields = ("id", "user", "post")


class ReactionCreateSerializer(ModelSerializer):
    class Meta(ReactionSerializer.Meta):
        pass

    def validate(self, attrs):
        request = self.context.get("request")
        post_pk = self.context.get("post_pk")

        if not request or not post_pk:
            raise ValidationError("The variables request and post_pk are required")

        if Reaction.objects.filter(user=request.user, post=post_pk).exists():
            raise ValidationError(
                f"Reaction already exists from user with ID {request.user.id}"
            )

        return attrs


class ReactionReadSerializer(ModelSerializer):
    class Meta:
        model = Reaction
        fields = ("id", "post", "user", "type")
        read_only_fields = fields
