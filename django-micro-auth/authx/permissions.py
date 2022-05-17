from authx.authentication import get_permission_data
from rest_framework.permissions import BasePermission

class PingTestPermission(BasePermission):
    def has_permission(self, request, view):
        permission_data = get_permission_data(
            request, 'ping'
        )
        
        return permission_data.get("permission")

class IsCashierUser(BasePermission):
    def has_permission(self, request, view):
        permission_data = get_permission_data(
            request, 'cashierpermission'
        )
        return permission_data.get("permission")


class IsBaristaUser(BasePermission):
    def has_permission(self, request, view):
        permission_data = get_permission_data(
            request, 'baristapermission'
        )
        return permission_data.get("permission")


class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        permission_data = get_permission_data(
            request, 'menagerpermission'
        )
        return permission_data.get("permission")


class IsOwnerUser(BasePermission):
    def has_permission(self, request, view):
        permission_data = get_permission_data(
            request, 'ownerpermission'
        )
        return permission_data.get("permission")


class MenuViewPermission(BasePermission):

    def __init__(self):
        self.permission_dict = None

    def fetch_permission(self, request):

        if self.permission_dict is None:
            permission_data = get_permission_data(
                request, 'menupermision'
            )
            self.permission_dict = permission_data
            return permission_data

        return self.permission_dict

    def has_permission(self, request, view):
        has_permission_dict = self.fetch_permission(
            request).get('has_permission')
        return has_permission_dict.get(view.action)

    def has_object_permission(self, request, view, obj):
        has_object_permission_dict = self.fetch_permission(
            request).get('has_object_permission')
        return has_object_permission_dict.get(view.action)
