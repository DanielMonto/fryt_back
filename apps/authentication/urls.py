from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny
from apps.authentication.views import UsersAPIView,MyTokenObtainPairView,ResetPasswordAPIView,ForgotPasswordAPIView,UserAuthAPIView
from rest_framework_simplejwt.views import TokenBlacklistView
from django.urls import path

class MyTokenRefreshView(TokenRefreshView):
    permission_classes=[AllowAny]

urlpatterns = [
    path('',UsersAPIView.as_view()),
    path('refresh/',MyTokenRefreshView.as_view()),
    path('login/',MyTokenObtainPairView.as_view()),
    path('reset_password/',ResetPasswordAPIView.as_view()),
    path('forgot_password/',ForgotPasswordAPIView.as_view()),
    path('logout/',TokenBlacklistView.as_view()),
    path('auth/',UserAuthAPIView.as_view())
]
