from rest_framework import permissions
from .models import SubAdmin

class IsAuthenticated(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        # return SubAdmin.id == request.user
        return obj.id == request.user.id or request.user.is_admin