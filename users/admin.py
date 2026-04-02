from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser
from . import models

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', "phone_number", 'is_active')
    fields = ('email', 'phone_number', 'password', 'is_active', 'is_staff', 'is_superuser')
    # Register your models here.
