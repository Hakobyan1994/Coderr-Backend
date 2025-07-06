from rest_framework import permissions
from django.shortcuts import get_object_or_404
from user_auth_app.models import Profile


class IsBusinessUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Jeder darf lesen.
        if not request.user.is_authenticated:
            return False  # Anonyme User dürfen nicht schreiben.
        
        profile = getattr(request.user, 'profile', None)
        return profile is not None and profile.user_type == 'business'



class IsOfferCreatorOrReadOnly(permissions.BasePermission):
    """
    Nur der Ersteller (creator) des Angebots darf es bearbeiten oder löschen.
    Andere Benutzer dürfen nur lesen (GET, HEAD, OPTIONS).
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user_profile = Profile.objects.filter(user=request.user).first()
        
        return (
            obj.creator == request.user and
            user_profile is not None and
            user_profile.user_type == 'business'
        )
