"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import path

from home.consumers import *


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django_application = get_asgi_application()

#a list to behave as routing.py file for routing the asgi routes... as the urls.py is used for wsgi routing. 
ws_patterns = [
    path("ws/test/", TestConsumer.as_asgi()),
]


application = ProtocolTypeRouter({
    'http' : django_application,
    'websocket' : AuthMiddlewareStack(URLRouter(ws_patterns)),                #the urls being routed will be registered in the websocket register
})

