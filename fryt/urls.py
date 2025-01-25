from django.urls import path,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/',include('apps.categorys.urls')),
    path('chat/',include('apps.chat.urls')),
    path('auth/',include('apps.authentication.urls')),
    path('notifications/',include('apps.notifications.urls')),
    path('users_relations/', include('apps.usersRelations.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
