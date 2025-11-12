from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_display', 'avatar_preview', 'is_newsletter_subscribed', 'created_at']
    list_filter = ['is_newsletter_subscribed', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['avatar_preview', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Details', {
            'fields': ('bio', 'avatar', 'avatar_preview')
        }),
        ('Preferences', {
            'fields': ('is_newsletter_subscribed',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_display(self, obj):
        """Display user with link to their posts count"""
        posts_count = obj.user.blog_posts.count()
        return format_html(
            '<strong>{}</strong> <span style="color: gray;">({} posts)</span>',
            obj.user.get_full_name() or obj.user.username,
            posts_count
        )
    user_display.short_description = 'User'
    
    def avatar_preview(self, obj):
        """Show avatar preview"""
        if obj.avatar:
            return format_html(
                '<img src="{}" width="100" height="100" style="border-radius: 8px; object-fit: cover;" />',
                obj.avatar.url
            )
        return 'No avatar'
    avatar_preview.short_description = 'Avatar Preview'


class UserProfileInline(admin.TabularInline):
    """Inline profile editing in User admin"""
    model = UserProfile
    can_delete = False
    fields = ['bio', 'avatar', 'is_newsletter_subscribed']


class EnhancedUserAdmin(BaseUserAdmin):
    """Enhanced User admin with profile info"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'date_joined']
    list_filter = BaseUserAdmin.list_filter + ('is_superuser', 'is_staff', 'is_active', 'date_joined')
    inlines = (UserProfileInline,)


# Unregister default UserAdmin and register enhanced version
admin.site.unregister(User)
admin.site.register(User, EnhancedUserAdmin)
