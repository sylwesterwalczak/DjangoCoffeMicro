import requests
from django.conf import settings
from rest_framework.authentication import get_authorization_header

import json

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from .jwt import decode_jwt

User = get_user_model()


def get_permission_data(request, path=None):
    try:
        headers = {"Authorization": get_authorization_header(request)}
        r = requests.get(f"{settings.AUTH_SERVER_PREFIX}/{path}",
                            headers=headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise Exception(err)
    except Exception as err:
        raise Exception(err)
    return r.json()


class TokenAuthentication(BaseAuthentication):
    """
    The correct verification returns a tuple (user token)
    """

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        token = request.META.get('HTTP_AUTHORIZATION')

        if token is None:
            return None

        segments = token.split('.')

        if len(segments) == 0:
            return None

        if len(segments) != 3:
            raise AuthenticationFailed(
                _("Authorization header must contain three space-delimited values"),
                code="bad_authorization_header",
            )

        if segments[1] is None:
            return None

        validated_token = decode_jwt(segments[1])
        return self.get_user(validated_token), validated_token

    def get_user(self, validated_token):
        """
        Method that returns a user based on a token.
        """

        res = json.loads(validated_token)
        try:
            user_id = res.get('id')
        except KeyError:
            raise ValidationError(_("No user id"))

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed(
                _("User not found"), code="user_not_found")

        if not user.is_active:
            raise AuthenticationFailed(
                _("User is inactive"), code="user_inactive")

        return user
