from django.contrib import admin
from .models import Category, Thread, Post

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'creator', 'created_at')
    list_filter = ('category', 'creator', 'created_at')
    search_fields = ('title', 'creator__username')

admin.site.register(Thread, ThreadAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'creator', 'created_at')
    list_filter = ('thread', 'creator', 'created_at')
    search_fields = ('content', 'creator__username')

admin.site.register(Post, PostAdmin)
