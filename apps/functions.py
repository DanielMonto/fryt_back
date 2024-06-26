import os
from functools import wraps
from django.conf import settings
from fryt.settings import BASE_DIR
from pywebpush import webpush, WebPushException
from apps.authentication.models import UserOwnModel
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

def send_notification(user, payload):
    subscriptions = user.subscription_notifications
    private_key = os.path.join(BASE_DIR,'private_key.pem')
    vapid_claims = settings.VAPID_CLAIMS
    for subscription in subscriptions:
        subscription_info = {
            "endpoint": subscription.endpoint,
            "keys": {
                "p256dh": subscription.p256dh,
                "auth": subscription.auth
            }
        }
        try:
            webpush(
                subscription_info,
                payload,
                private_key,
                vapid_claims
            )
        except WebPushException:
            return 'Push failed'

def get_user_from_access(request):
    user=UserOwnModel.objects.filter(id=AccessToken(request.META['HTTP_AUTHORIZATION'].split(' ')[1]).payload['user']['id']).first()
    return user

def are_keys_in_dict(dict,*keys):
    '''
        Checks if all the keys are in dict 
    '''
    missing_keys=[key for key in keys if key not in dict]
    if not missing_keys:
        return (True, 'All keys in dict',None)
    if len(missing_keys)==1:
        return (False, f'Key {missing_keys[0]} is required',missing_keys[0])
    if len(missing_keys)==2:
        return (False, f'Keys {missing_keys[0]} and {missing_keys[1]} are required',str('/'.join(missing_keys)))
    message=', '.join(missing_keys[:-1]) + f', and {missing_keys[-1]} keys are required'
    return (False,str(message),str('/'.join(missing_keys)))

def check_user_exists(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = get_user_from_access(request)
        if user:
            return func(request, *args, **kwargs)
        else:
            return Response({'message': 'User does not exist'}, status=401)
    return wrapper