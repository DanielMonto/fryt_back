from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Category, CategoryType
from .serializers import CategorySerializer, CategoryTypeSerializer
from apps.functions import are_keys_in_dict
from rest_framework.views import APIView

class CategoryAdminAPIView(APIView):
    '''
        View for creation updating and deleting for a category
    '''
    permission_classes = [IsAdminUser]

    def post(self, request):
        '''
            Post method, manages the creation of a category
        '''
        # Checks if the keys are provided and if not return the right error_message
        key_safes, error_message, field = are_keys_in_dict(request.data, 'category_name', 'category_types')
        if key_safes:
            category_name = request.data['category_name']
            categories_using_category_name = Category.objects.filter(name=category_name)
            if len(categories_using_category_name) == 0:
                category = Category(name=category_name)
                category_saved_successfully, message = category.set_category_types(request.data['category_types'])
                return Response({'message': message}, status=200 if category_saved_successfully else 400)
            return Response({'message': f'Category name {category_name} is being used', 'field': 'category_name'}, status=400)
        return Response({'message': error_message, 'field': field}, status=400)

    def delete(self, request):
        '''
            Manage deleting process for a category 
        '''
        key_safes, error_message, field = are_keys_in_dict(request.data, 'category_name')
        if key_safes:
            category_name = request.data['category_name']
            categories_using_category_name = Category.objects.filter(name=category_name)
            if len(categories_using_category_name) != 0:
                category = categories_using_category_name[0]
                category.delete()
                return Response({'message': f'Category {category_name} deleted successfully'}, status=200)
            return Response({'message': f'Category {category_name} does not exist', 'field': 'category_name'}, status=400)
        return Response({'message': error_message, 'field': field}, status=400)
    
    def put(self, request):
        '''
            Manage updating process for a category 
        '''
        key_safes, error_message, field = are_keys_in_dict(request.data, 'category_name', 'new_category_name')
        if key_safes:
            category_name = request.data['category_name']
            new_category_name = request.data['new_category_name']
            categories_using_category_name = Category.objects.filter(name=category_name)
            if len(categories_using_category_name) != 0:
                category = categories_using_category_name[0]
                category.name = new_category_name
                category.save()
                return Response({'message': f'Category {category_name} updated successfully'}, status=200)
            return Response({'message': f'Category {category_name} does not exist', 'field': 'category_name'}, status=400)
        return Response({'message': error_message, 'field': field}, status=400)

class CategoryNormalAPIView(APIView):
    '''
        View for retrieving all categories
    '''
    def get(self, request):
        '''
            Get method, retrieves all categories
        '''
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({'categories': serializer.data})
    
class CategoryTypeAdminAPIView(APIView):
    '''
        View for creation updating and deleting for a category_type
    '''
    permission_classes = [IsAdminUser]

    def post(self, request):
        '''
            Post method, manages the creation of a category
        '''
        key_safes, error_message, field = are_keys_in_dict(request.data, 'category_type_name')
        if key_safes:
            category_type_name = request.data['category_type_name']
            categories_using_category_type_name = CategoryType.objects.filter(name=category_type_name)
            if len(categories_using_category_type_name) == 0:
                category = CategoryType(name=category_type_name)
                category.save()
                return Response({'message': f'Category type {category_type_name} saved successfully'}, status=200)
            return Response({'message': f'Category type name {category_type_name} is being used', 'field': 'category_type_name'}, status=400)
        return Response({'message': error_message, 'field': field}, status=400)
    
    def delete(self, request):
        '''
            Manage deleting process for a category 
        '''
        key_safes, error_message, field = are_keys_in_dict(request.data, 'category_type_name')
        if key_safes:
            category_type_name = request.data['category_type_name']
            categories_using_category_type_name = CategoryType.objects.filter(name=category_type_name)
            if len(categories_using_category_type_name) != 0:
                category = categories_using_category_type_name[0]
                category.delete()
                return Response({'message': f'Category {category_type_name} deleted successfully'}, status=200)
            return Response({'message': f'Category {category_type_name} does not exist', 'field': 'category_type_name'}, status=400)
        return Response({'message': error_message, 'field': field}, status=400)
    
    def put(self, request):
        '''
            Manage updating process for a category type
        '''
        key_safes, error_message, field = are_keys_in_dict(request.data, 'category_type_name', 'new_category_type_name')
        if key_safes:
            category_type_name = request.data['category_type_name']
            new_category_type_name = request.data['new_category_type_name']
            categories_using_category_type_name = CategoryType.objects.filter(name=category_type_name)
            if len(categories_using_category_type_name) != 0:
                category = categories_using_category_type_name[0]
                category.name = new_category_type_name
                category.save()
                return Response({'message': f'Category type {category_type_name} updated successfully'}, status=200)
            return Response({'message': f'Category type {category_type_name} does not exist', 'field': 'category_type_name'}, status=400)
        return Response({'message': error_message, 'field': field}, status=400)

class CategoryTypeNormalAPIView(APIView):
    '''
        View for retrieving all categories
    '''
    def get(self, request):
        '''
            Get method, retrieves all categories
        '''
        categories = CategoryType.objects.all()
        serializer = CategoryTypeSerializer(categories, many=True)
        return Response(serializer.data)