from rest_framework import permissions
from user_auth_app.models import Profile
from django.shortcuts import get_object_or_404



class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True      
        return obj.user == request.user