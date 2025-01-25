from django.contrib import admin
from .models import Chat, ChatGroup, ChatGroupMembership
# Register your models here.
admin.site.register(Chat)
admin.site.register(ChatGroup)
admin.site.register(ChatGroupMembership)