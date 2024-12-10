from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Define an inline admin descriptor for Profile model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

# Define a new User Admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('pk', 'username', 'name', 'is_staff', 'is_active', 'is_superuser')

    def name(self, obj):
        return obj.profile.name

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone')

