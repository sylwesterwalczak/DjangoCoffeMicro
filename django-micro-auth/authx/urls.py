from django.urls.conf import path

from .views import PingTestView

urlpatterns = [

    path('check/',
         PingTestView.as_view(), name='check')
]
