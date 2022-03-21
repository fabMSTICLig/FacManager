from rest_framework import permissions
from django.contrib.auth import get_user_model


class IsAdminOrIsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        isself = False
        if isinstance(obj, get_user_model()):
            isself = request.user == obj
        else:
            isself = request.user == obj.user
        return request.user.is_staff or isself


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.method in permissions.SAFE_METHODS

class IsMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.members.filter(pk=request.user).exists()

class RGPDAccept(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rgpd_accept is not None
