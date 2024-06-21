from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny
from .views import UsersAPIView,LogInAPIView,ResetPasswordAPIView,ForgotPasswordAPIView,UserAuthAPIView,IsRefreshTokenValidAPIView
from django.urls import path

class MyTokenRefreshView(TokenRefreshView):
    permission_classes=[AllowAny]

urlpatterns = [
    path('',UsersAPIView.as_view()),
    path('refresh_token/',MyTokenRefreshView.as_view()),
    path('login/',LogInAPIView.as_view()),
    path('reset_password/',ResetPasswordAPIView.as_view()),
    path('forgot_password/',ForgotPasswordAPIView.as_view()),
    path('auth/',UserAuthAPIView.as_view()),
    path('refresh_valid/',IsRefreshTokenValidAPIView.as_view())
]
