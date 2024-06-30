import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
# unknown error
# display as relative path is not same as you expect
from mysite import routings  # 自定义的路由

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# application = get_asgi_application() # 注释掉这行，改为 http 和 websocket 同时使用
application = ProtocolTypeRouter({
    'http': get_asgi_application(),  # http 访问时，使用默认路由
    'websocket': URLRouter(routings.websocket_urlpatterns),  # websocket 访问时，使用自定义路由
})
