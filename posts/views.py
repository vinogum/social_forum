from rest_framework import viewsets, permissions
from .serializers import PostCreateSerializer, PostListSerializer
from .models import Post


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None
    queryset = Post.objects.all()

    def get_serializer_class(self):
        serializers = {
            "create": PostCreateSerializer,
            "list": PostListSerializer,
        }
        serializer = serializers.get(self.action, self.serializer_class)
        return serializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)