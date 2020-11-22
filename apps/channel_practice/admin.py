from django.contrib import admin

# Register your models here.
from apps.channel_practice.models import Notice, Ip

admin.site.register(Notice)
admin.site.register(Ip)