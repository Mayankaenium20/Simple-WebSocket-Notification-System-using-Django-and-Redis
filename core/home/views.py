from django.shortcuts import render
from django.http import HttpResponse
import time
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.


def home(request):

    for i in range(1, 10):
        
        channel_layer = get_channel_layer()
        data = {"count" : i}

        async_to_sync(channel_layer.group_send)(  
            "test_consumer_group",
            {"type": "send_notification", "value": json.dumps(data)},
        )

        time.sleep(2)

    return HttpResponse()

# async def home(request):

#     for i in range(1, 10):
        
#         channel_layer = get_channel_layer()
#         data = {"count" : i}

#         await(channel_layer.group_send)(  
#             "new_consumer_group",                                                 #name of the function changed as per the new class.
#             {"type": "send_notification", "value": json.dumps(data)},
#         )

#         time.sleep(2)

#     return HttpResponse()
