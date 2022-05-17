from django.urls import re_path
from django.urls.conf import include, path

from rest_framework.routers import DefaultRouter

from .viewsets import (
    UserViewSet,
    LoginView,
    ActivationUserEmailView,
    CheckPermissionView,
    CheckBaristaPermissionView,
    CheckCashierPermissionView,
    CheckManagerPermissionView,
    CheckOwnerPermissionView,
    MenuPermissionView
)

router = DefaultRouter()

router.register(
    r'users',
    UserViewSet,
    basename="users",
)

urlpatterns = [
    re_path(r'', include(router.urls)),
    path('login', LoginView.as_view(), name='login'),
    path('activate/<slug:uidb64>/<slug:token>/',
         ActivationUserEmailView.as_view(), name='activate'),
    path('check/',
         CheckPermissionView.as_view(), name='check'),

    path('baristapermission', CheckBaristaPermissionView.as_view(),
         name="baristapermission"),
    path('cashierpermission', CheckCashierPermissionView.as_view(),
         name="cashierpermission"),
    path('menagerpermission', CheckManagerPermissionView.as_view(),
         name="menagerpermission"),
    path('ownerpermission', CheckOwnerPermissionView.as_view(),
         name="ownerpermission"),
    path('menupermision', MenuPermissionView.as_view(), name="menupermision"),
]
