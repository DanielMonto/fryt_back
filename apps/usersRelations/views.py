from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FriendshipApplication
from .serializers import FriendshipApplicationSerializer
from rest_framework_simplejwt.tokens import AccessToken
from apps.functions import are_keys_in_dict, check_user_exists
from django.db.models import Q
from apps.authentication.models import UserOwnModel
from apps.authentication.serializers import UserSerializer

class FollowAPIView(APIView):
    '''
        Manage the retrieving of follows and followers, the new follow and nofollow
    '''
    @check_user_exists
    def get(self, request:HttpRequest, user = None):
        '''
            Retrieves all the users you have followed
        '''
        follows = user.follows.all()
        serializer = UserSerializer(follows, many=True)
        return Response({'follows':serializer.data}, status=200)

    @check_user_exists
    def post(self, request:HttpRequest, user = None):
        '''
            Manage the process of a new follow from user
        '''
        keys_safe, message, field = are_keys_in_dict(request.data, 'user_to_follow')
        if keys_safe:
            user_to_follow = UserOwnModel.objects.filter(username = request.data['user_to_follow']).first()
            if user_to_follow == None:
                return Response({'message':f'User {request.data['user_to_follow']} does not exist', 'field':'user_to_follow'}, status=400)
            user_to_follow.followers.add(user)
            user_to_follow.int_followers=len(user_to_follow.followers.all())
            user_to_follow.save()
            user.follows.add(user_to_follow)
            user.int_follows=len(user.follows.all())
            user.save()
        return Response({'message':message, 'field':field}, status=400)

    @check_user_exists
    def put(self, request:HttpRequest, user = None):
        '''
            Manage the retrieving of followers
        '''
        followers = user.followers.all()
        serializer = UserSerializer(followers, many = True)
        return Response({'followers':serializer.data}, status=200)

    @check_user_exists
    def delete(self, request:HttpRequest, user = None):
        '''
            Manage the nofollow from user to other
        '''
        keys_safes, message, field = are_keys_in_dict(request.data, 'user_to_nofollow')
        if keys_safes:
            user_to_nofollow = UserOwnModel.objects.filter(username = request.data['user_to_nofollow']).first()
            if user_to_nofollow == None:
                return Response({'message':'User to nofollow does not exist', 'field':'user_to_nofollow'}, status=400)
            user_to_nofollow.followers.remove(user)
            user_to_nofollow.int_followers=len(user_to_nofollow.followers.all())
            user_to_nofollow.save()
            user.follows.remove(user_to_nofollow)
            user.int_follows=len(user.follows.all())
            user.save()
            return Response({'message':f'User {user_to_nofollow.username} nofollow successfully'}, status=200)
        return Response({'message':message, 'field':field}, status=400)

class FriendshipsApplicationsAPIView(APIView):
    '''
        Management of retrieving, deleting, creating a friendship application
    '''
    @check_user_exists
    def get(self, request:HttpRequest, user = None):
        '''
            Manage the retrieving process of applications to me
        '''
        friend_applications = user.applications_to_me.all()
        serializer = FriendshipApplicationSerializer(friend_applications, many=True)
        return Response({'applications':serializer.data}, status=200)

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
                    'message':f'User to apply {request.data['user_to_apply']} does not exist',
                    'field': 'user_to_apply'
                }, status=400)
            is_valid_application = FriendshipApplication.application_is_valid(user, user_to_apply)
            # checking if there is already one FriendshipApplication with user as applicator and user_to_apply as applied
            if is_valid_application:
                new_friend_application = FriendshipApplication(applicator = user, applied = user_to_apply)
                new_friend_application.save()
                return Response({'message':'Application created successfully'}, status=200)
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
                    applicator.friends.add(user)
                    applicator.int_friends=len(applicator.friends.all())
                    applicator.save()
                    user.friends.add(applicator)
                    user.friends=len(user.friends.all())
                    user.save()
                    friendship_application.delete()
                    return Response({'message':f'Application from {applicator_username} accepted'}, status=200)
                return Response({
                    'message':'Applicator does not exist, could not accept application',
                    'field':'applicator'
                }, status=400)
            return Response({'message':f'Application from {applicator_username} does not exist', 'field':'applicator'}, status=400)
        return Response({'message':message, 'field':field}, status=400)

    def delete(self, request:HttpRequest):
        '''
            Management the delete of an FriendshipApplication
        '''
        keys_safes, message, field = are_keys_in_dict(request.data, 'other_user')
        if keys_safes:
            username = AccessToken(request.META['HTTP_AUTHORIZATION'].split(' ')[1]).payload['user']['username']
            friendship_application = FriendshipApplication.objects.filter(
                (Q(applied__username = request.data['other_user']) 
                    &
                Q(applicator__username = username))
                    |
                (Q(applied__username = username) 
                    &
                Q(applicator__username = request.data['other_user']))
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
        keys_safes, message, field = are_keys_in_dict(request.data,'friend_to_delete')
        if keys_safes:
            friend_to_delete = user.friends.filter(username=request.data['friend_to_delete']).first()
            if friend_to_delete == None:
                return Response({'message':f'User {request.data['friend_to_delete']} does not exist'}, status=400)
            friend_to_delete.int_friends = len(friend_to_delete.friends.all())
            friend_to_delete.save()
            user.int_friends = len(user.friends.all())
            user.save()
            return Response({'message':f'User {user.username} and {friend_to_delete.username}'})
        return Response({'message':message,'field':field}, status=400)

class SuggestionAPIView(APIView):
    '''
        Manage the get from the suggestions of friendships
    '''
    # TODO: do well recommendations based on liked things from user
    @check_user_exists
    def get(self, request:HttpRequest, user = None):
        '''
            Manage the get from right suggestions to friendships
        '''
        users = UserOwnModel.objects.exclude(username = user.username)
        serializer = UserSerializer(users, many=True)
        return Response({'suggestions':serializer.data}, status=200)