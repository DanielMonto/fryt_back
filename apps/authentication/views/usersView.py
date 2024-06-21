from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpRequest
from functions import are_keys_in_dict
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from models import UserOwnModel
from serializers import UserSerializer

class UsersAPIView(APIView):
    '''
        User crud management
    '''
    # Personalization of permissions for an unlogged client can register
    permission_classes = [AllowAny]
    def get(self,request):
        users=UserOwnModel.objects.all()
        serializer=UserSerializer(users,many=True)
        return Response(serializer.data)
    def post(self, request: HttpRequest):
        '''
            Manage the registering of an user
        '''
        # Checks if all the keys are in dict
        keys_safe, error_message, field = are_keys_in_dict(request.data, 'username', 'password', 'email')
        if keys_safe:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            # Checks if username or email have an user
            username_or_email_used, error_message, field = UserOwnModel.email_or_username_used(username, email)
            if not username_or_email_used:
                # Checks if the password is correct
                password_safe, error_message = UserOwnModel.safe_password(password)
                if password_safe:
                    # Saves the user and returns its information
                    user = UserOwnModel(email=request.data['email'], username=request.data['username'], password=make_password(password))
                    user.save()
                    serializer = UserSerializer(user, many=False)
                    return Response(serializer.data, status=200)
                # Password incorrect, returns the right error_message (seen in UserOwnModel.safe_password function)
                return Response({'message': error_message, 'field': 'password'}, status=400)
            # Username or email used, with right error_message (seen in UserOwnModel.email_or_username_used function)
            return Response({'message': error_message, 'field': field}, status=400)
        # One or more keys (username, password, email) are not provided by the client, with the right error_message (seen in are_keys_in_dict function)
        return Response({'message': error_message, 'field': field}, status=400)
    def delete(self,request):
        '''
            Manage the logout process
        '''
        key_safes, error_message, field = are_keys_in_dict(request.data, 'refresh_token')
        if key_safes:
            try:
                refresh_token = RefreshToken(request.data['refresh_token'])
            except TokenError:
                return Response({'message':'Token invalid'},status=200)
            refresh_token.blacklist()
            return Response({'message':'Token invalided'},status=200)
        return Response({'message': error_message, 'field': 'refresh_token'}, status=400)