"""
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
"""

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
