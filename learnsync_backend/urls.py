"""learnsync_backend URL Configuration
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from graphene_django.views import GraphQLView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
    path('learnsync/', include('learnsync_app.urls')),
    path('accounts/', include('accounts.urls')),
    path('forum/',include('forum.urls')),
    path('subscription/', include('subscription.urls')),


]


# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
