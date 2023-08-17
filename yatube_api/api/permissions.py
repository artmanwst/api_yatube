from django.http import HttpRequest

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Возвращает True если метод в составе permissions.SAFE_METHODS
    либо пользователь является автором контента
    """
    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request: HttpRequest, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsStuffOrReadOnly(permissions.BasePermission):
    """
    Возвращает True если метод в составе permissions.SAFE_METHODS
    либо пользователь является администратором
    """
    message = 'Изменеие контента разрешено только администрации!'

    def has_object_permission(self, request: HttpRequest, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
        )
