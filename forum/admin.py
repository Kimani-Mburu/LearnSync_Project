from django.contrib import admin
from .models import Category, Thread, Post, Conversion, UserFeedback, UserActivity

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'thread_count')

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'creator', 'created_at', 'view_count', 'upvotes')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'creator', 'created_at', 'view_count', 'upvotes', 'sentiment_score', 'likes', 'calculate_replies')

    def calculate_replies(self, obj):
        """
        Display the number of replies for a post.
        """
        return obj.calculate_replies()

    calculate_replies.short_description = 'Replies'  # Custom column header

@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):
    list_display = ('user', 'conversion_type', 'timestamp')

@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp')

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'timestamp', 'ip_address')
