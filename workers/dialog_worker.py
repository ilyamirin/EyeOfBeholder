from channels.consumer import SyncConsumer
from channels.layers import get_channel_layer

server_channel_layer = get_channel_layer("server")