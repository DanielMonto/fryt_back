from rest_framework.serializers import ModelSerializer
from ..models import UserOwnModel

class UserSerializer(ModelSerializer):
    '''
        User serializer
    '''
    class Meta:
        model=UserOwnModel
        fields='__all__'