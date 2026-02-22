from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # User must be authenticated
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow read-only methods
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow write only if user is owner
        return obj.user_name == request.user      # user_name from model