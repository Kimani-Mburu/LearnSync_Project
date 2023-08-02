from django.urls import path
from . import views

app_name = 'learnsync_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search_results'),
    path('search_suggestions/', views.search_suggestions, name='search_suggestions'),
    path('dashboard/', views.DashboardView.as_view(), name='user_dashboard'),
    # Combined View URL (Detail View and Download Paper)
    path('paper/<slug:slug>/', views.CombinedView.as_view(), name='paper_detail'),


    ]
