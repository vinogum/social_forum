from rest_framework.views import Response, APIView
from .serializers import UserSerializer
from rest_framework import permissions
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import viewsets


class RegisterView(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_user = User.objects.filter(
            username=serializer.validated_data["username"]
        ).exists()
        if is_user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
