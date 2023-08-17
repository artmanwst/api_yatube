from django.shortcuts import get_object_or_404

from rest_framework import status, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response

from posts.models import (
    Post,
    Group,
    Comment,
    Follow
    )
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
        PostSerializer,
        GroupSerializer,
        CommentSerializer,
        FollowSerializer
    )


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer: PostSerializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def create(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer: CommentSerializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['user__username', 'following__username']

    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer: FollowSerializer):
        serializer.save(user=self.request.user)
