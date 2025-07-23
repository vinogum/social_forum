from rest_framework import viewsets, permissions, mixins
from posts.serializers import (
    PostWriteSerializer,
    ImageWriteSerializer,
    PostReadSerializer,
    CommentSerializer,
    ReactionSerializer,
    ReactionCreateSerializer,
    ReactionReadSerializer,
    PostUpdateSerializer,
)
from django.shortcuts import get_object_or_404
from rest_framework import parsers
from posts.models import Post, Comment, Reaction
from posts.permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    serializer_class = PostReadSerializer
    queryset = Post.objects.all()

    def get_serializer_class(self):
        serializers = {
            "create": PostWriteSerializer,
            "list": PostReadSerializer,
            "retrieve": PostReadSerializer,
            "update": PostUpdateSerializer,
            "partial_update": PostUpdateSerializer,
        }
        return serializers.get(self.action, self.serializer_class)

    def get_queryset(self):
        user_pk = self.kwargs.get("user_pk")
        if user_pk:
            return Post.objects.filter(user_id=user_pk)
        return Post.objects.all()

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)

        files = self.request.FILES.getlist("images")
        images_data = [{"image_data": file} for file in files]

        images_serializer = ImageWriteSerializer(data=images_data, many=True)
        images_serializer.is_valid(raise_exception=True)
        images_serializer.save(post=post)


class CommentViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Comment.objects.all()

    def get_queryset(self):
        post_pk = self.kwargs.get("post_pk")
        if post_pk is not None:
            return Comment.objects.filter(post_id=post_pk)
        return Comment.objects.all()

    def perform_create(self, serializer):
        post_pk = self.kwargs.get("post_pk")
        post = get_object_or_404(Post, id=post_pk)
        serializer.save(user=self.request.user, post=post)


class ReactionViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = ReactionReadSerializer
    queryset = Reaction.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        post_pk = self.kwargs.get("post_pk")
        if post_pk:
            return Reaction.objects.filter(post=post_pk)
        return Reaction.objects.all()
    
    def get_serializer_class(self):
        if self.action in ["update", "delete"]:
            return ReactionSerializer
        elif self.action == "create":
            return ReactionCreateSerializer
        else: return self.serializer_class
    
    def get_serializer_context(self):
        context = {"request": self.request, "post_pk": self.kwargs.get("post_pk")}
        return context

    def perform_create(self, serializer):
        post_pk = self.kwargs.get("post_pk")
        post = get_object_or_404(Post, id=post_pk)
        serializer.save(user=self.request.user, post=post)
