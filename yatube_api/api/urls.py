from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from api.views import CommentViewSet, GroupViewSet, PostViewSet

router = SimpleRouter()
router.register('api/v1/posts', PostViewSet)
router.register('api/v1/groups', GroupViewSet)
router.register(r'api/v1/posts/(?P<pk1>[^/.]+)/comments', CommentViewSet)


urlpatterns = [
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]
