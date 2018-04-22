# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pydoc import locate

from django.conf import settings
from rest_framework.permissions import BasePermission, IsAdminUser


class IsSuperUser(BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class UsersAdminPermissions(BasePermission):
    """
    Allows access to either of permissions.
    """
    users_admin_permission_class_name = getattr(settings, 'USES_ADMIN_PERMISSION', None)
    users_admin_permission_class = None
    if users_admin_permission_class_name:
        users_admin_permission_class = locate(users_admin_permission_class_name)
    elif users_admin_permission_class_name != "":
        users_admin_permission_class = IsAdminUser
    if users_admin_permission_class:
        permission_classes = (IsSuperUser, users_admin_permission_class)
    else:
        permission_classes = (IsSuperUser, )

    def has_permission(self, request, view):
        for permission in [permission() for permission in self.permission_classes]:
            if permission.has_permission(request, self):
                return True
        return False
