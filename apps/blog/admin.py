from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Post, Comment, Reaction, Newsletter


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_display', 'posts_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']

    def color_display(self, obj):
        """Display category color as a colored square"""
        return format_html(
            '<div style="width: 30px; height: 30px; background-color: {}; border-radius: 4px; border: 1px solid #ddd;"></div>',
            obj.color
        )
    color_display.short_description = 'Color'

    def posts_count(self, obj):
        """Show number of posts in this category"""
        return obj.posts.count()
    posts_count.short_description = 'Posts'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'published_at', 'views_count', 'featured']
    list_filter = ['status', 'category', 'featured', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'excerpt']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'category')
        }),
        ('Content', {
            'fields': ('content', 'excerpt', 'featured_image')
        }),
        ('Publishing', {
            'fields': ('status', 'is_visible', 'featured', 'published_at', 'scheduled_publish_at')
        }),
        ('Metadata', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Filter posts based on user permissions"""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Staff users can only see their own posts
            return qs.filter(author=request.user)
        return qs
    
    def save_model(self, request, obj, form, change):
        """Set author to current user if not already set"""
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author__username', 'content', 'post__title']
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        """Approve selected comments"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comment(s) approved.')
    approve_comments.short_description = 'Approve selected comments'
    
    def disapprove_comments(self, request, queryset):
        """Disapprove selected comments"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comment(s) disapproved.')
    disapprove_comments.short_description = 'Disapprove selected comments'


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'reaction_type', 'created_at']
    list_filter = ['reaction_type', 'created_at']
    search_fields = ['user__username', 'post__title']
    readonly_fields = ['created_at', 'post', 'user', 'reaction_type']
    
    def has_add_permission(self, request):
        """Disable manual creation of reactions"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion of reactions"""
        return True


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    readonly_fields = ['subscribed_at']
    
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    def activate_subscribers(self, request, queryset):
        """Activate selected subscribers"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} subscriber(s) activated.')
    activate_subscribers.short_description = 'Activate selected subscribers'
    
    def deactivate_subscribers(self, request, queryset):
        """Deactivate selected subscribers"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} subscriber(s) deactivated.')
    deactivate_subscribers.short_description = 'Deactivate selected subscribers'
