from django.contrib import admin
from userauths.models import User, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'is_active']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'phone', 'image']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
