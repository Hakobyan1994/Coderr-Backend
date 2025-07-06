from rest_framework import permissions

class IsCustomerUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Jeder darf lesen.
        if not request.user.is_authenticated:
            return False  # Anonyme User dürfen nicht schreiben.
        
        profile = getattr(request.user, 'profile', None)
        return profile is not None and profile.user_type == 'customer'