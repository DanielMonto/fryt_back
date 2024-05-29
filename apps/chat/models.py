from django.db import models
from apps.authentication.models import UserOwnModel

class Chat(models.Model):
    '''
        Model for private chat between two users
    '''
    user_1=models.ForeignKey(UserOwnModel,default=None,on_delete=models.SET_NULL,related_name='user_1_chats',null=True,blank=True)
    user_2=models.ForeignKey(UserOwnModel,default=None,on_delete=models.SET_NULL,related_name='user_2_chats',null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)

class ChatGroup(models.Model):
    '''
        Model for the chat of groups and its management
    '''
    members=models.ManyToManyField(UserOwnModel,through='ChatGroupMembership',through_fields=("chat","user"))
    name=models.CharField(max_length=250,unique=True)
    created=models.DateTimeField(auto_now_add=True)

class ChatGroupMembership(models.Model):
    '''
        Model that represents the relation between in members from ChatGroup tu users
    '''
    user=models.ForeignKey(UserOwnModel,on_delete=models.CASCADE)
    chat=models.ForeignKey(ChatGroup,on_delete=models.CASCADE)
    date_user_joined=models.DateTimeField(auto_now_add=True)