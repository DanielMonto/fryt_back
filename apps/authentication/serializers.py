from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserOwnModel
from rest_framework.serializers import ModelSerializer

## Serializers from the classes for easier management in the views

class UserSerializer(ModelSerializer):
    '''
        User serializer
    '''
    class Meta:
        model=UserOwnModel
        fields='__all__'

class LogInWithEmailSerializer(TokenObtainPairSerializer):
    '''
        Serializer used for authentication specifically login with email
    '''
    @classmethod
    def get_token(cls, user:UserOwnModel):
        '''
            Get base unencrypted for user jwt
        '''
        token=super().get_token(user)
        token['user']={
            'id':str(user.id),
            'email':user.email,
            'username':user.username,
            'is_staff':user.is_staff,
            'is_guest':user.guest
        }
        return token

class LogInWithUsernameSerializer(TokenObtainPairSerializer):
    '''
        Serializer used for authentication specifically login with username
    '''
    @classmethod
    def get_token(cls, user:UserOwnModel):
        '''
            Get base unencrypted for user jwt
        '''
        token=super().get_token(user)
        token['user']={
            'id':str(user.id),
            'email':user.email,
            'username':user.username,
            'is_staff':user.is_staff,
            'is_guest':user.guest
        }
        return token