from asgiref.sync import async_to_sync, sync_to_async
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer

from django.core.exceptions import ObjectDoesNotExist

from apps.channel_practice.models import Ip


class MyConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name="dashboard"
        await self.channel_layer.group_add(self.group_name,self.channel_name,)
        await self.accept()



    async def disconnect(self, code):
       await self.channel_layer.group_discard(
           self.group_name,self.channel_name
       )

    async def receive(self, text_data):

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'deprocessing',
                'data':text_data,
            }

        )

        print('>>>>',text_data)


    async def deprocessing(self,event):

        await self.send(event['data'])



class TestConsumer(AsyncWebsocketConsumer):
    groupname = 'notice'

    async def connect(self):
        #getting ip address of client
        self.ip=self.scope['client'][0]


        try:
            #check ip already available in database
           self.device= sync_to_async(Ip.objects.get)(address=self.ip)
        except ObjectDoesNotExist:
            #if ip address not exist raise error
            raise DenyConnection("Invalid User")

        await self.channel_layer.group_add(self.groupname, self.channel_name)
        await self.accept()
        print(self.scope['client'][0])

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.groupname,self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        await self.channel_layer.group_send(
            self.groupname,{
                'type':'rahi',
                'data':text_data,
            }
        )
        print(">>>",text_data)

    async def rahi(self,event):
        await self.send(event['data'])

    #comes from models post_save signal
    async def sendNotice(self,event):
        await self.send(text_data=event['notice'])

