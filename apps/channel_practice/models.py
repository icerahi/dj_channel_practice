from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Notice(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Ip(models.Model):
    address = models.GenericIPAddressField()

    def __str__(self):
        return str(self.address)


#if modeel save it signal will send data to django channel
@receiver(post_save,sender=Notice)
def post_save_notice(sender,instance,created,**kwargs):
    if created:
        #getting channel layer
        channel_layer=get_channel_layer()
        #async function convert to sync and added the channel groupname and data
        async_to_sync(channel_layer.group_send)(
            'notice',{
                'type':'sendNotice',
                'notice':str(instance.name)
            }
        )