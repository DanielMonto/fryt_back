from django.contrib import admin
from .models import UserOwnModel, PasswordResetRequest
# Register your models here.
admin.site.register(UserOwnModel)
admin.site.register(PasswordResetRequest)