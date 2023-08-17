from rest_framework import routers

from django.urls import include, path

from api.views import (
    PostViewSet,
    GroupViewSet,
    CommentViewSet,
    FollowViewSet
)

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register('follow', FollowViewSet)
router.register('posts/(?P<post_id>\\d+)/comments', CommentViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
