from django.contrib import admin
from .models import UserProfile, Tag, Category, ResearchPaper, Reference, ThesisPaper, Author
from django.contrib.admin.widgets import FilteredSelectMultiple

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'gender', 'get_interests', 'created_at', 'updated_at']
    list_filter = ['gender', 'interests', 'created_at', 'updated_at']
    search_fields = ['user__username', 'full_name', 'bio']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'full_name', 'bio', 'profile_image', 'social_site_urls')
        }),
        ('Personal Information', {
            'fields': ('gender', 'interests')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    ordering = ['user__username']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')

    def user_info(self, obj):
        return f'{obj.user.username} - {obj.user.email}'

    def get_interests(self, obj):
        return ", ".join([interest.name for interest in obj.interests.all()])

    get_interests.short_description = 'Interests'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'interests':
            kwargs['widget'] = FilteredSelectMultiple('Interests', is_stacked=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name']
    
class ReferenceInline(admin.TabularInline):
    model = Reference

@admin.register(ResearchPaper)
class ResearchPaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'publication_date', 'views']
    list_filter = ['category', 'publication_date']
    search_fields = ['title', 'abstract']
    ordering = ['title']
    inlines = [ReferenceInline]

@admin.register(ThesisPaper)
class ThesisPaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'publication_date', 'views']
    list_filter = ['category', 'publication_date']
    search_fields = ['title', 'description']
    ordering = ['title']
    inlines = [ReferenceInline]

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['content', 'research_paper', 'thesis_paper']
    search_fields = ['content']