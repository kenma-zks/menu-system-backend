from rest_framework import permissions

class IsAuthenticated(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.id == view.kwargs['pk'] or request.user.is_admin:
                return True
            return False

        
    