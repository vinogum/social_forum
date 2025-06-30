from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import PostViewSet, CommentViewSet, ReactionAPIView
from django.urls import path, include


posts_router = DefaultRouter()
posts_router.register("", PostViewSet, basename="post")
post_comments_router = NestedDefaultRouter(posts_router, "", lookup="post")
post_comments_router.register(r"comments", CommentViewSet)


urlpatterns = [
    path("<int:post_pk>/react/", ReactionAPIView.as_view()),
    path("", include(posts_router.urls)),
    path("", include(post_comments_router.urls)),
]
