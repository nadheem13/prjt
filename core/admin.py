from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_provider', 'is_learner', 'bio', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_provider', 'is_learner', 'bio', 'profile_picture')}),
    )
    list_display = ('username', 'email', 'is_provider', 'is_learner', 'is_staff')
    list_filter = ('is_provider', 'is_learner', 'is_staff', 'is_superuser')

admin.site.register(User, CustomUserAdmin)
