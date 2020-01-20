from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

from FRS.consumers import StreamConsumer
from workers.consumers import FaceRecognitionConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r'^stream1/', StreamConsumer),
                ]
            )
        )
    ),
    'channel': ChannelNameRouter({
        'recognizefaces': FaceRecognitionConsumer,
    }),
})
