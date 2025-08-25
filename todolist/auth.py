from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access')
        if not access_token:
            return None  # no token → unauthenticated
        # pass the token to the parent class for validation
        try:
            validated_token = self.get_validated_token(access_token)
        except AuthenticationFailed:
            return None
        return self.get_user(validated_token), validated_token