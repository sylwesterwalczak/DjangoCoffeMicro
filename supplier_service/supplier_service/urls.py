from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authx.urls')),
    path('rest-api/v1/', include('supplier_service.api')),
]

