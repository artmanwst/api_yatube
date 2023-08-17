from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Group, Post, Comment, Follow


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", 
                                          read_only=True)

    class Meta:
        model = Post
        fields = ("id", "text", "author", "pub_date", "group")
        read_only_fields = ("posts", "author")

    def get_author(self, obj):
        return obj.author.username


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", 
                                          read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "created", "post")
        read_only_fields = ("post", "author")


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
        )

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=('user', 'following'),
            message='Вы уже подписаны'
            )]

        def validate(self, data):
            if data.users == data.following:
                raise serializers.ValidationError(
                    'Нельзя быть подписаным на самого себя'
                    )
            return data
