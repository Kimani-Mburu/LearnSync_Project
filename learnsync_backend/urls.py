"""learnsync_backend URL Configuration
"""
from django.contrib import admin
from django.urls import include, path
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
    path('learnsync/', include('learnsync_app.urls')),
    path('accounts/', include('accounts.urls')),


]
