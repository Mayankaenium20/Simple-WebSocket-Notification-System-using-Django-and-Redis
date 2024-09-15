from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync              #initially the code is asynchronous, but we need to implement the wrapper function to make it asynchronous


import json

from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class TestConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):                    #backend to frontend data sending
        self.room_group_name = "test_consumer_group"

        await self.channel_layer.group_add(
            self.room_group_name,   
            self.channel_name         #adding the group labels to the channels layer. Channel name is used for identifying the connection
        )

        await self.accept()

        text_data = json.dumps({'status': 'connected. May here!'})
        await self.send(text_data)  # Send data back to the frontend in JSON format



    async def receive(self, text_data):             #front to backend data sending
        print(text_data)                            #data printed here
        await self.send(text_data = json.dumps({'status' : 'Data recieved!'}))

    async def disconnect(self, *args, **kwargs):
        print("Disconnected")

    async def send_notification(self, event):
        print("NOTIF SENT!")

        data = json.loads(event.get('value'))
        await self.send(text_data = json.dumps({'payload' : data}))




"""
The ports of the django's dev server and uvicorn server are different.
Hence use different ports for both of them, eg 8000 default for django and 8001 for uvicorn. Updates will be seen on the uvicorn server. 
The uvicorn server needs to be restarted everytime a change is made in the code. 
"""