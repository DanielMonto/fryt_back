from django.urls import path,include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/',include('apps.categorys.urls')),
    path('auth/',include('apps.authentication.urls')),
    path('notifications/',include('apps.notifications.urls'))
]
