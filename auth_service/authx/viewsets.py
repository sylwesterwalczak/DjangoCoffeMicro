from datetime import datetime, timedelta

from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from authx.permissions import IsOwnerUser

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response

from .serializers import UserSerializer
from .jwt import create_jwt

User = get_user_model()


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        logout(request)
        self.perform_destroy(instance)
        return Response(status=HTTP_204_NO_CONTENT)

    def send_auth_emial(self, user):
        current_site = get_current_site(self.request)
        domain = current_site.domain,
        uid = urlsafe_base64_encode(force_bytes(user.pk)),
        token = default_token_generator.make_token(user)

        mail_subject = _('Activate your blog account.')
        protocol = 'http'

        url = f"{ protocol }://{ domain[0] }/rest-api/v1/authx/activate/{uid[0]}/{token}"
        message = f'<p><a href="{ url }">{ url }</a></p>'

        email = EmailMessage(mail_subject, message, to=[user.email])

        email.send()

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = False
        user.save()

        self.send_auth_emial(user)


class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed(_('User not found!'))

        if not user.check_password(password):
            raise AuthenticationFailed(_('Incorrect password!'))

        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow()
        }

        token = create_jwt(payload)
        return Response({'jwt': token})


class ActivationUserEmailView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, uidb64, token):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(_('Thank you for your email confirmation. Now you can login your account.'), status=HTTP_204_NO_CONTENT)
        else:
            return Response(_('Activation link is invalid!'), status=HTTP_204_NO_CONTENT)


class CheckPermissionView(APIView):
    """
    Check if user has Owner role
    """

    def get(self, request, format=None):
        perm = bool(request.user.is_authenticated and request.user.role == 4)
        return Response({"permission": perm})


class CheckBaristaPermissionView(APIView):
    """
    Check if user has Barista role
    """

    def get(self, request, format=None):
        perm = bool(request.user.is_authenticated and request.user.role >= 2)
        return Response({"permission": perm})


class CheckCashierPermissionView(APIView):
    """
    Check if user has Cashier role
    """

    def get(self, request, format=None):
        perm = bool(request.user.is_authenticated and request.user.role >= 1)
        return Response({"permission": perm})


class CheckManagerPermissionView(APIView):
    """
    Check if user has Manager role
    """

    def get(self, request, format=None):
        perm = bool(request.user.is_authenticated and request.user.role >= 3)
        return Response({"permission": perm})


class CheckOwnerPermissionView(APIView):
    """
    Check if user has Owner role
    """

    def get(self, request, format=None):
        perm = bool(request.user.is_authenticated and request.user.role == 4)
        return Response({"permission": perm})


class MenuPermissionView(APIView):
    """
    Check MenuPermission
    """

    def get(self, request, format=None):
        permission = bool(request.user.is_authenticated and request.user.role >= 1)
        permission_2 = bool(request.user.is_authenticated and request.user.role >= 2)
        return Response({
            "has_permission": {
                "retrieve": permission,
                "list": permission,
            },
            "has_object_permission": {
                "retrieve": permission,
                "update": permission_2,
                "partial_update": permission_2,
                "destroy": permission_2,
                "create": permission_2,
            }
        })

