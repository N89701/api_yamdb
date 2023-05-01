from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin
        return request.method in permissions.SAFE_METHODS


class IsOwnerOrAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return request.user.is_authenticated
        if request.method in ('PATCH', 'DELETE'):
            return (obj.author == request.user
                    or request.user.is_admin
                    or request.user.is_moderator)
        return request.method in permissions.SAFE_METHODS


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin
        return False
