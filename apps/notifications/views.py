from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SubscriptionNotificationModel
from apps.functions import are_keys_in_dict, check_user_exists

class SubscribeBrowserAPIView(APIView):
    @check_user_exists
    def post(self, request, user = None):
        key_safes, message, field = are_keys_in_dict(request.data, 'auth', 'endpoint', 'p256dh')
        if key_safes:
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
        return Response({'message':message,'field':field},status=400)