from rest_framework.permissions import BasePermission


class TeamPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'GET', 'DELETE']:
            if request.user.role.role == 'gestion':
                return True
