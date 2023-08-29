from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is a manager
        return request.user.role == 'Manager'
