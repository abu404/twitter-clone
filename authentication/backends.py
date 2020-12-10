import jwt
from rest_framework import authentication
from django.conf import settings
from rest_framework import exceptions
from django.contrib.auth.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request, username=None, password=None, email=None):
        auth_header = authentication.get_authorization_header(request)
        if not auth_header:
            return None
        token = auth_header.decode('utf-8').split(" ")[1]
        try:
            decoded_token = jwt.decode(token, settings.JWT_SECRET)
            user = User.objects.get(username=decoded_token['username'])
            return user, decoded_token
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed("Your token is not valid.")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Your token has expired. Please login in again.')
