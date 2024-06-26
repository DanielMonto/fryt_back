from rest_framework.response import Response
from .models import Chat, ChatGroup, ChatGroupMembership
from apps.authentication.models import UserOwnModel
from .serializers import ChatGroupMembershipSerializer, ChatGroupSerializer, ChatSerializer
from rest_framework_simplejwt.tokens import AccessToken
from apps.functions import are_keys_in_dict,check_user_exists
from django.db.models import Q
from rest_framework.views import APIView

class ChatAPIView(APIView):
    @check_user_exists
    def get(self, request, user = None):
        chats=Chat.objects.filter(Q(user_1=user) or Q(user_2=user))
        serializer=ChatSerializer(chats,many=True)
        return Response({'chats':serializer.data},status=200)

class ChatGroupAPIView(APIView):
    pass

class ChatGroupMembershipAPIView(APIView):
    pass