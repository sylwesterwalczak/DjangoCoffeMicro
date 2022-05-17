from rest_framework.views import APIView

from authx.permissions import PingTestPermission
from rest_framework.response import Response


class PingTestView(APIView):
    """
    Test connection
    """
    permission_classes = [PingTestPermission]

    def get(self, request, format=None):
        return Response({"status": "OK", 'user': request.user.username})

