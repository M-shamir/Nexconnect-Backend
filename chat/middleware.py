# chat/middleware.py
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        from django.contrib.auth import get_user_model  # ✅ move inside method
        User = get_user_model()  # ✅ define inside method

        headers = dict(scope["headers"])
        cookie_header = headers.get(b'cookie', b'').decode()
        cookies = {
            k.strip(): v for k, v in [
                pair.split('=') for pair in cookie_header.split('; ') if '=' in pair
            ]
        }

        token = cookies.get("access_token")
        if token is None:
            scope["user"] = AnonymousUser()
            return await super().__call__(scope, receive, send)

        try:
            validated_token = UntypedToken(token)
            user_id = validated_token.get("user_id")
            user = await database_sync_to_async(User.objects.get)(id=user_id)
        except Exception:
            user = AnonymousUser()

        close_old_connections()
        scope["user"] = user
        return await super().__call__(scope, receive, send)
