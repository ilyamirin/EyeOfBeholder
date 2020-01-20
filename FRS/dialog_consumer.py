from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from channels.layers import get_channel_layer
from string import ascii_letters
import random
import copy
import time
import asyncio

clock_channel_layer = get_channel_layer("clock")
face_channel_layer = get_channel_layer("face")


def is_image(bytes_data):
    pref = bytes_data[:100]
    for suff in b'PNG', b'JPG', b'JPEG', b'JFIF', b'JPE':
        if suff in pref:
            return True
    return False


class DialogServerConsumer(AsyncWebsocketConsumer):
    groups = ["recognize-faces", "dialog-recognize-faces"]

    def __init__(self, *args):
        super().__init__(*args)
        self.uid = "".join(random.choice(ascii_letters) for _ in range(8))
        self.dialog_uid = ""

    async def sync_clock(self):
        while True:
            message = {"type": "sync_clock", "timestamp": time.time(), "uid": self.uid}
            try:
                await asyncio.gather(
                    clock_channel_layer.send("recognizefaces", message),
                    self.send(json.dumps(message)),
                )
                print("sync clock", flush=True)
            except Exception as e:
                print('sync clock exception: ' + str(e))
            await asyncio.sleep(4)

    async def connect(self):
        await self.accept()
        asyncio.get_event_loop().create_task(self.sync_clock())

    async def dialog_faces_ready(self, message):
        if message["uid"] == self.uid:
            if message.get("dialog_uid", "") != "":
                self.dialog_uid = message["dialog_uid"]
            await self.send(json.dumps(message))

    async def faces_ready(self, message):
        if message["uid"] == self.uid:
            res = copy.deepcopy(message)
            res['type'] = 'face'
            await self.send(json.dumps(res))

    async def receive(self, text_data=None, bytes_data=None):
        try:
            print(f"{self.uid}: receive {len(text_data) if text_data else 0} text data, {len(bytes_data) if bytes_data else 0} bytes data")
            if bytes_data and len(bytes_data) > 0:
                if is_image(bytes_data):
                    await face_channel_layer.send("recognizefaces",
                                                  {"type": "recognize", "bytes_data": bytes_data, "uid": self.uid, "dialog": True})
        except Exception as e:
            print(e)

    async def disconnect(self, close_code):
        print("disconnect ", close_code)
