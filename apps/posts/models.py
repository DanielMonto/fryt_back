from django.db import models
from apps.authentication.models import UserOwnModel
# from apps.categorys.models import Category
from apps.chat.models import Chat,ChatGroup

# Create your models here.
class Message(models.Model):
    user=models.ForeignKey(UserOwnModel,on_delete=models.SET_NULL, blank=True, null=True)
    text=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    chat=models.ForeignKey(Chat,on_delete=models.CASCADE)
    image=models.URLField(default=None, null=True, blank=True)
    audio=models.URLField(default=None, null=True, blank=True)
    video=models.URLField(default=None, null=True, blank=True)

class MessageGroup(models.Model):
    user=models.ForeignKey(UserOwnModel,on_delete=models.SET_NULL, blank=True, null=True)
    text=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    image=models.URLField(default=None, null=True, blank=True)
    audio=models.URLField(default=None, null=True, blank=True)
    video=models.URLField(default=None, null=True, blank=True)
    chat_group=models.ForeignKey(ChatGroup,on_delete=models.CASCADE)

class Post(Message):
    pass