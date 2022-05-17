from django.urls import re_path

from .consumers import PurchaseConsumer

websocket_urlpatterns = [
    re_path(r'ws/purchase/(?P<room_name>\w+)/$', PurchaseConsumer.as_asgi()),
]