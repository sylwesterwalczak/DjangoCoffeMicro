from django.urls.conf import include
from django.urls import re_path

from rest_framework.routers import DefaultRouter

from .viewsets import (
    MenuView,
    MenuItemView,
    ComponentView
)
router = DefaultRouter()

router.register(
    r'menu',
    MenuView,
    basename="menu"
)
router.register(
    r'items', MenuItemView,
    basename="menu"
)
router.register(
    r'components', ComponentView,
    basename="menu"
)


urlpatterns = [
    re_path(r'', include(router.urls)),
]
