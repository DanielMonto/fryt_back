from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import UserOwnModel
from django.http import HttpRequest
from apps.functions import are_keys_in_dict
from ..serializers import getTokensSerializer


class LogInAPIView(TokenObtainPairView):
    '''
        View for obtaining access and refresh tokens
    '''
    # Personalization of permissions for an unlogged client can login
    permission_classes = [AllowAny]
    serializer_class = getTokensSerializer
    def post(self, request: HttpRequest):
        '''
            Post method for obtaining the tokens
        '''
        # Checks if all the keys are in dict
        key_safes, error_message, field = are_keys_in_dict(request.data, 'email', 'password')
        if key_safes:
            email = request.data['email']
            # Checks if there is an user with client email
            users = UserOwnModel.objects.filter(email=email)
            if len(users) != 0:
                password = request.data['password']
                user = users[0]
                # Checks if the client´s provided password is correct
                if user.check_password(password):
                    request.data['username'] = user.username
                    return super().post(request)
                # Incorrect password
                return Response({'message': 'incorrect password', 'field': 'password'}, status=400)
            # Email unused
            return Response({'message': f'email {email} unused', 'field': 'email'}, status=400)
        # Email or password fields unprovided
        return Response({'message': error_message, 'field': field}, status=400)