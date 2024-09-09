from django.urls import path
from .views import FriendshipsApplicationsAPIView, FriendshipsAPIView, FollowAPIView, SuggestionAPIView

urlpatterns = [
    path('friends/',FriendshipsAPIView.as_view()),
    path('friends_applications/',FriendshipsApplicationsAPIView.as_view()),
    path('follows/',FollowAPIView.as_view()),
    path('suggestions/',SuggestionAPIView.as_view())
]