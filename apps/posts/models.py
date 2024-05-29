from django.db import models
from apps.authentication.models import UserOwnModel
# from apps.categorys.models import Category
from apps.chat.models import Chat,ChatGroup

# Create your models here.
class Message(models.Model):
    user=models.ForeignKey(UserOwnModel,on_delete=models.CASCADE)
    text=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    chat=models.ForeignKey(Chat,on_delete=models.CASCADE)
    is_image=models.BooleanField(default=False)
    is_audio=models.BooleanField(default=False)
    is_video=models.BooleanField(default=False)
    url=models.URLField(default=None,null=True,blank=True)

class MessageGroup(models.Model):
    user=models.ForeignKey(UserOwnModel,on_delete=models.CASCADE)
    text=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    is_image=models.BooleanField(default=False)
    is_audio=models.BooleanField(default=False)
    is_video=models.BooleanField(default=False)
    url=models.URLField(default=None,null=True,blank=True)
    chat_group=models.ForeignKey(ChatGroup,on_delete=models.CASCADE)

class Post(Message):
    pass