from django.urls import path
from .consumers import PrivateUsersChatConsumer

websocket_urlpatterns=[
    path('ws/private_users_chat/<str:chat_id>/', PrivateUsersChatConsumer.as_asgi())
]