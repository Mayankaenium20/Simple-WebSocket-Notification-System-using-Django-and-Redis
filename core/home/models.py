from django.db import models
from django.contrib.auth.models import User
import json


#importing the channel layers:
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from channels.generic.websocket import AsyncJsonWebsocketConsumer
# Create your models here.

##########################################################################
"""

This is the basic class and it's working perfectly alright. Just uncomment it and use it with an external websocket service

"""

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    notification = models.TextField(max_length = 100)
    is_seen = models.BooleanField(default = False)


    #overriding the save method as it is being handled by the signalling concept. this step is irrelevant for the future use as this is usually implemented using signals
    def save(self, *args, **kwargs):
        print("Save fn called!")

        channel_layer = get_channel_layer()
        notification_objs = Notification.objects.filter(is_seen = False).count()
        data = {
            'count' : notification_objs, 
            'current_notification' : self.notification
        }

        async_to_sync(channel_layer.group_send)(                #here everything is working synchronously, so await and async are not used here. instead aysync is converted into sync for execution
            'test_consumer_group', {
                'type' : 'send_notification',
                'value' : json.dumps(data)
            }
        )


        super(Notification, self).save(*args, **kwargs)