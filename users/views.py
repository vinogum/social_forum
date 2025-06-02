from rest_framework.views import Response, APIView
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.models import User


class RegisterView(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=serializer.validated_data["username"])
        if user.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
