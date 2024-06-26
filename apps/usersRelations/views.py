from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FriendshipApplication
from .serializers import FriendshipApplicationSerializer
from rest_framework_simplejwt.tokens import AccessToken
from apps.functions import are_keys_in_dict, check_user_exists
from apps.authentication.models import UserOwnModel
from apps.authentication.serializers import UserSerializer

class FriendshipsApplicationsAPIView(APIView):
    '''
        Management of retrieving, deleting, creating a friendship application
    '''
    @check_user_exists
    def get(self, request:HttpRequest, user = None):
        '''
            Manage the retrieving process of applications to and from me
        '''
        keys_safes, message, field = are_keys_in_dict(request.data, 'to_me')
        if keys_safes:
            to_me = request.data['to_me']
            if to_me:
                # applications from me
                friend_applications = user.applications_from_me.all()
            else:
                # applications to me
                friend_applications = user.applications_to_me.all()
            serializer = FriendshipApplicationSerializer(friend_applications, many=True)
            return Response({'applications':serializer.data}, status=200)
        return Response({'message':message, 'field':field})

    @check_user_exists
    def post(self, request:HttpRequest, user = None):
        '''
            Manage the application creation from me
        '''
        keys_safes, message, field = are_keys_in_dict(request.data,'user_to_apply')
        if keys_safes:
            user_to_apply = UserOwnModel.objects.filter(username = request.data['user_to_apply']).first()
            if user_to_apply == None:
                # User to apply never existed or was deleted
                return Response({
                    'message':f'User to apply {request.data['user_to_apply']} does not exist'
                }, status=400)
            is_valid_application = FriendshipApplication.application_is_valid(user, user_to_apply)
            # checking if there is already one FriendshipApplication with user as applicator and user_to_apply as applied
            if is_valid_application:
                new_friend_application = FriendshipApplication(applicator = user, applied = user_to_apply)
                new_friend_application.save()
                return Response({'message':'Application created successfully'})
            return Response({'message':'Application already exist'}, status=200)
        return Response({'message':message, 'field':field}, status=400)

    @check_user_exists
    def put(self, request:HttpRequest, user = None):
        '''
            Manage the accepting process of an application
        '''
        keys_safes, message, field = are_keys_in_dict(request.data, 'applicator')
        if keys_safes:
            applicator_username = request.data['applicator']
            friendship_application = FriendshipApplication.objects.filter(
                applicator__username = applicator_username,
                applied = user
            ).first()
            if friendship_application:
                applicator = UserOwnModel.objects.filter(username = applicator_username).first()
                if applicator:
                    user.friends.add(applicator)
                    applicator.friends.add(user)
                    return Response({'message':f'Application from {applicator_username} accepted'}, status=200)
                return Response({
                    'message':'Applicator does not exist,could not accept application',
                    'field':'applicator'
                }, status=400)
            return Response({'message':f'Application from {applicator_username} does not exist'})
        return Response({'message':message, 'field':field}, status=400)

    def delete(self, request:HttpRequest):
        '''
            Management the delete of an application of friendship either is from me or to me
        '''
        keys_safes, message, field = are_keys_in_dict(request.data, 'am_i_applied', 'other_user')
        if keys_safes:
            am_i_applied = request.data['am_i_applied']
            username = AccessToken(request.META['HTTP_AUTHORIZATION'].split(' ')[1]).payload['user']['username']
            if am_i_applied:
                friendship_application = FriendshipApplication.objects.filter(
                    applicator__username = request.data['other_user'],
                    applied__username = username
                ).first()
            else:
                friendship_application = FriendshipApplication.objects.filter(
                    applied__username = request.data['other_user'],
                    applicator__username = username
                ).first()
            if friendship_application:
                friendship_application.delete()
            return Response({'message':'Friend application deleted'}, status=200)
        return Response({'message':message, 'field':field}, status=400)

class FriendshipsAPIView(APIView):
    '''
        Manage the retrieving of friends and unfriend process
    '''
    @check_user_exists
    def get(self, request:HttpRequest, user = None):
        '''
            Manage the retrieving of all friend of user
        '''
        friends = user.friends.all()
        serializer = UserSerializer(friends, many=True)
        return Response({'friends':serializer.data}, status=200)

    @check_user_exists
    def delete(self, request:HttpRequest, user = None):
        '''
            Manage the unfriend process
        '''
        keys_safes, message, field = are_keys_in_dict(request.data, 'friend')
        if keys_safes:
            friend = user.friends.filter(username = request.data['friend']).first()
            if friend:
                friend.friends.remove(user)
                user.friends.remove(friend)
            return Response({'message':f'{user.username} and {request.data['friend']} are not friends anymore'}, status=200)
        return Response({'message':message, 'field':field}, status=400)