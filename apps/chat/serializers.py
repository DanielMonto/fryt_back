from rest_framework.serializers import ModelSerializer
from .models import Chat,ChatGroup,ChatGroupMembership

class ChatSerializer(ModelSerializer):
    class Meta:
        model=Chat
        fields='__all__'

class ChatGroupSerializer(ModelSerializer):
    class Meta:
        model=ChatGroup
        fields='__all__'

class ChatGroupMembershipSerializer(ModelSerializer):
    class Meta:
        model=ChatGroupMembership
        fields='__all__'