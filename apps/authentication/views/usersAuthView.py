from rest_framework.views import APIView
from apps.functions import are_keys_in_dict
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from ..models import UserOwnModel
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response

class UserAuthAPIView(APIView):
    def delete(self,request):
        '''
            Manage delete process from an user
        '''
        key_safes, error_message, field = are_keys_in_dict(request.data, 'refresh_token')
        if key_safes:
            user_id=AccessToken(request.META['HTTP_AUTHORIZATION'].split(' ')[1]).payload['user']['id']
            user=UserOwnModel.objects.filter(id=user_id).first()
            if user:
                user.delete()
                try:
                    refresh_token = RefreshToken(request.data['refresh_token'])
                except TokenError:
                    return Response({'message':'User delete token invalid'},status=200)
                refresh_token.blacklist()
                return Response({'message':'User deleted'},status=200)
            return Response({'message':'User deleted'},status=200)
        return Response({'message': error_message, 'field': 'refresh_token'}, status=400)