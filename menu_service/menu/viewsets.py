from rest_framework.viewsets import ModelViewSet
from authx.permissions import MenuViewPermission
# from utils.mixins import CustomLoggingViewSetMixin


from .serializers import (
    CreateComponentSerializer,
    CreateMenuItemSerializer,
    CreateMenuSerializer,
    MenuSerializer,
    CashierMenuSerializer,
    MenuItemSerializer,
    ComponentSerializer,
    AdminMenuSerializer,
    CashierMenuItemSerializer,
    ManagerMenuItemSerializer,
    ManagerComponentSerializer
)
from .models import Menu, MenuItem, Component


class MenuView(ModelViewSet):

    queryset = Menu.objects.all()
    permission_classes = [MenuViewPermission]

    def get_serializer_class(self):
        if self.request.user.role == 1:
            return CashierMenuSerializer
        elif self.request.user.role >= 3:
            if self.action in ['update', 'partial_update', 'create']:
                return CreateMenuSerializer
            return AdminMenuSerializer
        else:
            if self.action in ['update', 'partial_update', 'create']:
                return CreateMenuSerializer
            return MenuSerializer


class MenuItemView(ModelViewSet):

    queryset = MenuItem.objects.all()
    permission_classes = [MenuViewPermission]

    def get_serializer_class(self):
        if self.request.user.role == 1:
            return CashierMenuItemSerializer
        elif self.request.user.role >= 3:
            if self.action in ['update', 'partial_update', 'create']:
                return CreateMenuItemSerializer
            return ManagerMenuItemSerializer
        else:
            if self.action in ['update', 'partial_update', 'create']:
                return CreateMenuItemSerializer
            return MenuItemSerializer


class ComponentView(ModelViewSet):

    queryset = Component.objects.all()
    permission_classes = [MenuViewPermission]

    def get_serializer_class(self):

        if self.request.user.role >= 3:
            if self.action in ['update', 'partial_update', 'create']:
                return CreateComponentSerializer
            return ManagerComponentSerializer
        else:
            return ComponentSerializer
