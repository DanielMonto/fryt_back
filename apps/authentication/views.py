from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpRequest
from rest_framework.permissions import AllowAny
from .models import UserOwnModel, PasswordResetRequest
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.template.loader import render_to_string
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.hashers import make_password
from apps.functions import are_keys_in_dict
from .serializers import UserSerializer, LogInWithEmailSerializer, LogInWithUsernameSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings

# compare https://docs.google.com/forms/d/e/1FAIpQLSfBDwhTN7l_lxel6p44GC5UD76XwcDojMsFy8BCKkwHbUrwlA/viewform?vc=0&c=0&w=1&flr=0

class LogInWithUsernameView(TokenObtainPairView):
    '''
        View for obtaining access and refresh tokens
    '''
    # Personalization of permissions for an unlogged client can login
    permission_classes = [AllowAny]
    serializer_class = LogInWithUsernameSerializer
    def post(self, request: HttpRequest):
        '''
            Post method for obtaining the tokens with username
        '''
        # Checks if all the keys are in dict
        key_safes, error_message, field = are_keys_in_dict(request.data, 'username', 'password')
        if key_safes:
            username = request.data['username']
            # Checks if there is an user with client username
            users = UserOwnModel.objects.filter(username=username)
            if len(users) != 0:
                password = request.data['password']
                user = users[0]
                # Checks if the client´s provided password is correct
                if user.check_password(password):
                    request.data['email'] = user.email
                    return super().post(request)
                # Incorrect password
                return Response({'message': 'incorrect password', 'field': 'password'}, status=400)
            # username unused
            return Response({'message': f'username {username} unused', 'field': 'username'}, status=400)
        # username or password fields unprovided
        return Response({'message': error_message, 'field': field}, status=400)

class LogInWithEmailView(TokenObtainPairView):
    '''
        View for obtaining access and refresh tokens
    '''
    # Personalization of permissions for an unlogged client can login
    permission_classes = [AllowAny]
    serializer_class = LogInWithEmailSerializer
    def post(self, request: HttpRequest):
        '''
            Post method for obtaining the tokens with email
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
            users = UserOwnModel.objects.filter(username=email)
            if not users:
                # Email and username unused
                return Response({'message': f'email {email} unused', 'field': 'email'}, status=400)
            password = request.data['password']
            user = users[0]
            # Checks if the client´s provided password is correct
            if user.check_password(password):
                request.data['username'] = user.username
                request.data['email'] = user.email
                return super().post(request)
            # Incorrect password
            return Response({'message': 'incorrect password', 'field': 'password'}, status=400)
        # Email or password fields unprovided
        return Response({'message': error_message, 'field': field}, status=400)

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

class CreateGuestUserAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        new_guest = UserOwnModel.create_guest_user()
        serializer = UserSerializer(new_guest, many=False)
        return Response({'user':serializer.data},status=200)

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