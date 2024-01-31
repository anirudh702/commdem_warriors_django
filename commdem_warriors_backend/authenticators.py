from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from user.models import UserModel


class ApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get("HTTP_AUTHORIZATION")
        print(f"api_key {api_key}")
        if not api_key:
            raise AuthenticationFailed("You are not authorized")
        try:
            api_key = str(api_key).split(" ")[1]
            print(f"api_key {api_key}")
            api_key_answer = UserModel.objects.get(api_key=api_key)
        except UserModel.DoesNotExist:
            raise AuthenticationFailed("Invalid API key")

        return (api_key_answer, None)
