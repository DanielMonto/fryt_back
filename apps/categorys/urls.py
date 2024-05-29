from django.urls import path 
from .views import CategoryAdminAPIView,CategoryNormalAPIView,CategoryTypeAdminAPIView,CategoryTypeNormalAPIView

urlpatterns=[
    path('',CategoryNormalAPIView.as_view()),
    path('ad/',CategoryAdminAPIView.as_view()),
    path('type/',CategoryTypeNormalAPIView.as_view()),
    path('type/ad/',CategoryTypeAdminAPIView.as_view())
]