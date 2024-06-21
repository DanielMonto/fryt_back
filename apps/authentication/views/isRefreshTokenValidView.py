from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from functions import are_keys_in_dict
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class IsRefreshTokenValidAPIView(APIView):
    '''
        Check if the refresh is valid
    '''
    permission_classes=[AllowAny]
    def post(self,request):
        '''
            Check if the refresh is valid
        '''
        keys_safe, error_message, field = are_keys_in_dict(request.data, 'refresh_token')
        # Check if keys are in the request
        if keys_safe:
            try:
                refreshToken=RefreshToken(request.data['refresh_token'])
                refreshToken.verify()
                return Response({'message':'Refresh token is valid'},status=200)
            except TokenError:
                return Response({'message':'Refresh token is invalid'},status=400)
        return Response({'message':error_message},status=400)