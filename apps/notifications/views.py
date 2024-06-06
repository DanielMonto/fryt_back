from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.models import UserOwnModel
from rest_framework_simplejwt.tokens import AccessToken
from .models import SubscriptionNotificationModel
from functions import are_keys_in_dict

class SubscribeBrowserAPIView(APIView):
    def post(self, request):
        key_safes, message, field = are_keys_in_dict(request.data, 'auth', 'endpoint', 'p256dh')
        if key_safes:
            user = UserOwnModel.objects.filter(id = AccessToken(request.META['HTTP_AUTHORIZATION'].split(' ')[1]).payload['user']['id']).first()
            if user:
                new_subscription = SubscriptionNotificationModel(
                    user = user,
                    auth = request.data['auth'],
                    endpoint = request.data['endpoint'],
                    p256dh = request.data['p256dh']
                )
                result = new_subscription.save()
                if result == 'Data used':
                    return Response(
                        {
                            'message':'Subscription exist with that data',
                            'field':'auth/endpoint/p256dh'
                        },status=400)
                return Response({'message':'Subscription added successfully'},status=200)
            return Response({'message':'User does not exist'},status=400)
        return Response({'message':message,'field':field},status=400)