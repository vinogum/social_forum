from django.urls import path, include
from .views import RegisterView


urlpatterns = [
    path("", include("rest_framework.urls")),
    path("signup/", RegisterView.as_view(), name="signup"),
]
