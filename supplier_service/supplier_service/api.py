from django.urls import path, re_path
from django.urls.conf import include
from rest_framework import permissions

urlpatterns = [
    path('supplier/', include('supplier.urls')),
]
