# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nexconnect.settings')
django_asgi_app = get_asgi_application()

# ✅ Use function to delay import of middleware
def get_application():
    from chat.middleware import JWTAuthMiddleware
    return ProtocolTypeRouter({
        "http": django_asgi_app,
        "websocket": SessionMiddlewareStack(
            JWTAuthMiddleware(
                URLRouter(chat.routing.websocket_urlpatterns)
            )
        ),
    })

application = get_application()
