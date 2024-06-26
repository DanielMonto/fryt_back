from rest_framework.serializers import ModelSerializer
from .models import FriendshipApplication

class FriendshipApplicationSerializer(ModelSerializer):
    class Meta:
        model = FriendshipApplication
        fields = '__all__'