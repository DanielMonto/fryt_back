import os
from django.conf import settings
from fryt.settings import BASE_DIR
from pywebpush import webpush, WebPushException

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