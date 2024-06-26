from django.urls import path
from .views import FriendshipsApplicationsAPIView, FriendshipsAPIView

urlpatterns = [
    path('friends/',FriendshipsAPIView.as_view()),
    path('friends_applications/',FriendshipsApplicationsAPIView.as_view())
]