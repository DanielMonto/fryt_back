from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from functions import are_keys_in_dict
from rest_framework_simplejwt.tokens import AccessToken
from models import UserOwnModel
from django.contrib.auth.hashers import make_password

class ResetPasswordAPIView(APIView):
    '''
        API View for handling password reset with the old password
    '''

    def post(self, request: HttpRequest):
        '''
            Handle reset password request
        '''
        keys_safe, error_message, field = are_keys_in_dict(request.data, 'old_password', 'new_password', 'new_password_confirmation')
        # Check if keys are in the request
        if keys_safe:
            old_password = request.data['old_password']
            new_password = request.data['new_password']
            new_password_confirmation = request.data['new_password_confirmation']
            user_email = AccessToken(request.META['HTTP_AUTHORIZATION'].split(' ')[1]).payload['user']['email']
            user = UserOwnModel.objects.filter(email=user_email).first()

            # Check if the old password is correct
            if user and user.check_password(old_password):
                # Check if the new password matches the confirmation
                if new_password == new_password_confirmation:
                    # Check if the new password is secure
                    password_safe, error_message = UserOwnModel.safe_password(new_password)
                    if password_safe:
                        user.password = make_password(new_password)
                        user.save()
                        return Response({'message': "Password changed successfully"}, status=200)
                    # New password not secure
                    return Response({'message': error_message, 'field': 'new_password'}, status=400)
                # New password and confirmation do not match
                return Response({'message': "New password and confirmation do not match", 'field': 'new_password_confirmation'}, status=400)
            # Old password incorrect
            return Response({'message': 'Incorrect old password', 'field': 'old_password'}, status=400)
        # Required fields not provided
        return Response({'message': error_message, 'field': field}, status=400)