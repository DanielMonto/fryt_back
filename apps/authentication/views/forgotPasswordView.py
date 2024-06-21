from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from models import UserOwnModel, PasswordResetRequest
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from functions import are_keys_in_dict
from django.utils.html import strip_tags
from django.conf import settings

class ForgotPasswordAPIView(APIView):
    '''
        API View for handling forgotten passwords
    '''
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest):
        '''
            Handle forgot password request
        '''
        keys_safe, error_message, field = are_keys_in_dict(request.data, 'email')
        if keys_safe:
            email = request.data['email']
            user = UserOwnModel.objects.filter(email=email).first()
            if user:
                # If there's no existing reset request or it's invalid, create a new one
                pass_res_req = PasswordResetRequest.objects.filter(user=user).first()
                if not pass_res_req or not PasswordResetRequest.is_valid_code(pass_res_req):
                    pass_res_req = PasswordResetRequest(user=user)
                    pass_res_req.save()
                
                # Prepare and send the reset email
                html_content = render_to_string('forgot_password.html', {'user': user, 'code': pass_res_req.code})
                text_content = strip_tags(html_content)
                email = EmailMultiAlternatives(
                    subject="Forgot password from fryt",
                    body=text_content,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[user.email]
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
                return Response({'message': 'Email sent'}, status=200)
            # Email not found
            return Response({'message': "Email not found", 'field': 'email'}, status=400)
        # Email field not provided
        return Response({'message': error_message, 'field': 'email'}, status=400)

    def put(self, request: HttpRequest):
        '''
            Handle reset password request
        '''
        keys_safe, error_message, field = are_keys_in_dict(request.data, 'user_code', 'new_password', 'new_password_confirmation')
        if keys_safe:
            code = request.data['user_code']
            new_password = request.data['new_password']
            new_password_confirmation = request.data['new_password_confirmation']
            
            # Check if the code is valid
            if PasswordResetRequest.is_valid_code(code):
                pass_res_req = PasswordResetRequest.objects.get(code=code)
                user = pass_res_req.user
                
                # Check if the new password matches the confirmation
                if new_password_confirmation == new_password:
                    # Check if the new password is secure
                    password_safe, error_message = UserOwnModel.safe_password(new_password)
                    if password_safe:
                        user.password = make_password(new_password)
                        user.save()
                        pass_res_req.delete()
                        return Response({'message': "Password changed successfully"}, status=200)
                    # New password not secure
                    return Response({'message': error_message, 'field': 'new_password'}, status=400)
                # New password and confirmation do not match
                return Response({'message': "New password and confirmation do not match", 'field': 'new_password_confirmation'}, status=400)
            # Invalid code
            return Response({'message': f"Code {code} is not valid", 'field': 'user_code'}, status=400)
        # Required fields not provided
        return Response({'message': error_message, 'field': field}, status=400)