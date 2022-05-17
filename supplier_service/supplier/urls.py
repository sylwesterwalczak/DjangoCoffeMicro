from django.urls.conf import include
from django.urls import re_path

from rest_framework.routers import DefaultRouter

from .viewsets import SupplierViewSet

router = DefaultRouter()

router.register(
    r'supplier',
    SupplierViewSet,
    basename="users",
)

urlpatterns = [
    re_path(r'', include(router.urls)),
]
