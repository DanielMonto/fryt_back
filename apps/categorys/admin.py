from django.contrib import admin
from .models import Category, CategoryType
# Register your models here.
admin.site.register(CategoryType)
admin.site.register(Category)