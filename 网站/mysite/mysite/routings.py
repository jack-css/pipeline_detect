from django.urls import path
import sys

# sys.path.insert(0, "../")
from polls import consumer

websocket_urlpatterns = [
    path('message/', consumer.Cons.as_asgi()),
]
