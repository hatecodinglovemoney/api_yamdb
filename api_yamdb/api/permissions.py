from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Доступно только для администратора."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsOwnerAdminModeratorOrReadOnly(permissions.BasePermission):
    """Доступно для создателя объекта, администратора, модератора,
    остальным только для чтения."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступно только администратору, остальным только для чтения."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))
