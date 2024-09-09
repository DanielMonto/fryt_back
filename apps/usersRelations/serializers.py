from rest_framework.serializers import ModelSerializer
from apps.authentication.serializers import UserSerializer
from .models import FriendshipApplication

class FriendshipApplicationSerializer(ModelSerializer):
    applicator = UserSerializer(read_only=True)
    applied = UserSerializer(read_only=True)
    class Meta:
        model = FriendshipApplication
        fields = '__all__'