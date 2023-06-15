from django.contrib import admin
from .models import Assignment, Category, ResearchPaper, Tag, ThesisPaper, UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'interests', 'created_at', 'updated_at']
    list_filter = ['gender', 'interests']
    search_fields = ['user__username', 'user__email']

admin.site.register(UserProfile, UserProfileAdmin)


@admin.register(ThesisPaper)
class ThesisPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug')
    search_fields = ('title', 'author__user__username')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('author', 'tags', 'category')

@admin.register(ResearchPaper)
class ResearchPaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_authors', 'category', 'published_date']
    list_filter = ['category', 'published_date']
    search_fields = ['title', 'authors__full_name', 'abstract']
    
    def get_authors(self, obj):
        return ", ".join([author.full_name for author in obj.authors.all()])
    get_authors.short_description = 'Authors'


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_by', 'uploaded_at']
    list_filter = ['uploaded_by']
    search_fields = ['title', 'uploaded_by__username']
    date_hierarchy = 'uploaded_at'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)
