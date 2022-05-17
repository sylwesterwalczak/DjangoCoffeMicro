from django.urls.conf import include, path
from django.urls import re_path

from rest_framework.routers import DefaultRouter
from .viewsets import PurchseListView, PurchseViewSet, CancellingPurchase

router = DefaultRouter()

router.register(
    r'purchase',
    PurchseViewSet,
    basename="purchase"
)

urlpatterns = [
    re_path(r'', include(router.urls)),
    path('purchase-list/',
         PurchseListView.as_view(), name='purchase_list'),
    path('purchase-cancel/<int:pk>/',
         CancellingPurchase.as_view(), name='purchase_cancel'),
]
