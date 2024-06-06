from django.urls import path
from .views import SubscribeBrowserAPIView

urlpatterns = [
    path('subscribe/', SubscribeBrowserAPIView.as_view())
]