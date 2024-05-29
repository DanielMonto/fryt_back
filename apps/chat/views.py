from rest_framework.response import Response
from .models import Chat, ChatGroup, ChatGroupMembership
from apps.authentication.models import UserOwnModel
from .serializers import ChatGroupMembershipSerializer, ChatGroupSerializer, ChatSerializer
from rest_framework_simplejwt.tokens import AccessToken
from apps.functions import are_keys_in_dict
from django.db.models import Q
from rest_framework.views import APIView

class ChatAPIView(APIView):
    def get(self,request):
        user=UserOwnModel.objects.get(id=AccessToken(request.META['HTTP_AUTHORIZATION'].split(' ')[1]).payload['user']['id'])
        chats=Chat.objects.filter(Q(user_1=user) or Q(user_2=user))
        serializer=ChatSerializer(chats,many=True)
        return Response(serializer.data)

class ChatGroupAPIView(APIView):
    pass

class ChatGroupMembershipAPIView(APIView):
    pass