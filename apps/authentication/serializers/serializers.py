from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    '''
        Serializer used for authentication specifically login
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
            'is_staff':user.is_staff
        }
        return token