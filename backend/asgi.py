"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack
from orders.consumers import CartConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_asgi_application()

ws_pattern = [
    path('ws/cart/<int:order_id>/', CartConsumer.as_asgi())
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(ws_pattern))
})