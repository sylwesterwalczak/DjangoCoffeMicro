from rest_framework.permissions import BasePermission


class IsCashierUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role >= 1)


class IsBaristaUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role >= 2)


class IsManagerUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role >= 3)


class IsOwnerUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 4)


class MenuViewPermission(BasePermission):

    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list']:
            return bool(request.user.is_authenticated and request.user.role >= 1)
        elif view.action in ['update', 'partial_update', 'destroy', 'create']:
            return bool(request.user.is_authenticated and request.user.role >= 2)

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return bool(request.user.is_authenticated and request.user.role >= 1)
        elif view.action in ['update', 'partial_update', 'destroy', 'create']:
            return bool(request.user.is_authenticated and request.user.role >= 2)


