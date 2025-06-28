from rest_framework import viewsets, permissions
from .serializers import PostWriteSerializer, ImageWriteSerializer, PostReadSerializer
from rest_framework import parsers
from .models import Post


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    queryset = Post.objects.all()

    def get_serializer_class(self):
        serializers = {
            "create": PostWriteSerializer,
            "list": PostReadSerializer,
            "retrieve": PostReadSerializer,
        }
        return serializers.get(self.action, PostReadSerializer)

    def get_queryset(self):
        user_pk = self.kwargs.get("user_pk")
        if user_pk:
            return Post.objects.filter(user_id=user_pk)
        return self.queryset

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)

        files = self.request.FILES.getlist("images")
        images_data = [{"image_data": file} for file in files]
        import pdb; pdb.set_trace()

        images_serializer = ImageWriteSerializer(data=images_data, many=True)
        images_serializer.is_valid(raise_exception=True)
        images_serializer.save(post=post)
