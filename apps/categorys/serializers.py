from rest_framework.serializers import ModelSerializer
from .models import Category, CategoryType

class CategorySerializer(ModelSerializer):
    '''
        Serializer for categories
    '''
    class Meta:
        fields='__all__'
        model=Category

class CategoryTypeSerializer(ModelSerializer):
    '''
        Serializer for category types
    '''
    class Meta:
        fields='__all__'
        model=CategoryType