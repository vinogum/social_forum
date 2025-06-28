from rest_framework_nested.routers import DefaultRouter
from .views import PostViewSet
from django.urls import path, include


posts_router = DefaultRouter()
posts_router.register("", PostViewSet, basename="post")


urlpatterns = [path("", include(posts_router.urls))]
