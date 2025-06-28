from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import RegisterView, UserReadOnlyViewSet
from posts.views import PostViewSet


users_router = DefaultRouter()
users_router.register("", UserReadOnlyViewSet)
user_posts_router = NestedDefaultRouter(users_router, "", lookup="user")
user_posts_router.register(r"posts", PostViewSet)


urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("", include(user_posts_router.urls)),
    path("", include(users_router.urls)),
]
