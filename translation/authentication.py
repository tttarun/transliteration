from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.response import Response
from decouple import config
from django.contrib.auth.models import User


class APIAuthentication(authentication.BaseAuthentication):
    """Authenticates on the basis of API key"""
    def authenticate_header(self, request):
        api_key = request.headers.get('X-API-KEY', None)
        if api_key is None:
            return None

    def authenticate(self, request):
        api_key = request.headers.get('X-API-KEY', None)
        if not api_key == config('X_API_KEY'):
            raise exceptions.AuthenticationFailed
        user = User.objects.first()
        return user, None
