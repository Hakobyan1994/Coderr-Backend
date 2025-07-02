from rest_framework import permissions
from django.shortcuts import get_object_or_404
from user_auth_app.models import Profile

class IsCustomerUser(permissions.BasePermission):

    def has_permission(self, request, view):
        # Erlaubt immer GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Hole das Profil des eingeloggten Benutzers
        profile = get_object_or_404(Profile, user=request.user)

        return profile.user_type == 'customer'