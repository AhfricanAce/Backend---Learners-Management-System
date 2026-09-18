from rest_framework import permissions

class IsInstructor(permissions.BasePermission):
    """
    Allows access only to users who have the INSTRUCTOR role. 
    """

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'INSTRUCTOR'
        )

class IsAdminUserRole(permissions.BasePermission):
    """
    Allows access only to users who have ADMIN role.
    """
    def has_permission(self, request,view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'ADMIN'
        )
