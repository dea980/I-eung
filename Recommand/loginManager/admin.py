from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, OAuthProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '사용자 프로필'

class OAuthProfileInline(admin.StackedInline):
    model = OAuthProfile
    extra = 0
    verbose_name_plural = 'OAuth 프로필'
    readonly_fields = ('access_token', 'refresh_token')

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, OAuthProfileInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(OAuthProfile)
class OAuthProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'oauth_user_id', 'created_at', 'updated_at')
    list_filter = ('provider', 'created_at')
    search_fields = ('user__username', 'oauth_user_id')
    readonly_fields = ('access_token', 'refresh_token')
    ordering = ('-created_at',)
