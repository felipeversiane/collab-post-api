from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class.

    This class extends the JWTAuthentication class from rest_framework_simplejwt
    and provides custom authentication logic.
    """

    def authenticate(self, request: Request):
        """
        Authenticate the request.

        :param request: The incoming HTTP request.
        :type request: rest_framework.request.Request
        :return: A tuple containing the user object and the token, or None if authentication fails.
        :rtype: tuple(User, UntypedToken) or None
        """
        try:
            header = self.get_header(request)

            if header is None:
                raw_token = request.COOKIES.get(settings.AUTH_COOKIE)
            else:
                raw_token = self.get_raw_token(header)

            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)

            return self.get_user(validated_token), validated_token
        except (InvalidToken, AuthenticationFailed):
            return None
