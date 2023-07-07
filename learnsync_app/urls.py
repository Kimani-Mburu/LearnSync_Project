from django.urls import path
from .views import DashboardView, HomeView, Detail

app_name = 'learnsync_app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='user_dashboard'),
    path('detailview/', Detail.as_view(), name='detailview')
]
