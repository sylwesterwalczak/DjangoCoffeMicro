import os
from rest_framework.serializers import (
    ModelSerializer,
    SlugRelatedField,
    PrimaryKeyRelatedField,
    ListField,
    IntegerField
)
from authx.utils import fetch_service_data
from .models import Menu, MenuItem, Component



class BaseComponentSerializer(ModelSerializer):
    def to_representation(self, instance):
        api_url = os.environ.get('STORY_SERVICE')
        ret = super().to_representation(instance)
        ret['ingredient'] = fetch_service_data(
            ret['ingredient'], api_url, False)

        return ret

    class Meta:
        model = Component
        fields = '__all__'


class BaseItemSerializer(ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class BaseMenuSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class ComponentSerializer(BaseComponentSerializer):
    pass


class ManagerComponentSerializer(BaseComponentSerializer):
    pass


class MenuItemSerializer(BaseItemSerializer):
    ingredients = ComponentSerializer(read_only=True, many=True)


class ManagerMenuItemSerializer(BaseItemSerializer):
    ingredients = ManagerComponentSerializer(read_only=True, many=True)


class CashierMenuItemSerializer(BaseItemSerializer):
    ingredients = ComponentSerializer(read_only=True, many=True)


class MenuSerializer(BaseMenuSerializer):
    items = MenuItemSerializer(read_only=True, many=True)


class AdminMenuSerializer(BaseMenuSerializer):
    items = ManagerMenuItemSerializer(read_only=True, many=True)


class CashierMenuSerializer(BaseMenuSerializer):
    items = CashierMenuItemSerializer(read_only=True, many=True)


class CreateMenuItemSerializer(BaseItemSerializer):
    ingredients = PrimaryKeyRelatedField(
        many=True,
        queryset=Component.objects.all()
    )


class CreateMenuSerializer(BaseMenuSerializer):
    items = PrimaryKeyRelatedField(
        many=True,
        queryset=MenuItem.objects.all()
    )


class CreateComponentSerializer(BaseComponentSerializer):
    ingredient = ListField(child=IntegerField())
