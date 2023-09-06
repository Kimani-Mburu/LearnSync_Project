from django.urls import path
from . import views

urlpatterns = [
    path('forum/', views.forum_view, name='forum_two'),
    path('forum/create_post/', views.create_post, name='create_post'),
    path('submit-feedback/', views.UserFeedbackFormView.as_view(), name='submit_feedback'),
    path('user-conversions/', views.UserConversionView.as_view(), name='user_conversions'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('analytics/', views.AnalyticsDashboardView.as_view(), name='analytics_dashboard'),
    path('trending-threads/', views.TrendingThreadsView.as_view(), name='trending_threads'),
    path('sentiment-analysis/', views.SentimentAnalysisView.as_view(), name='sentiment_analysis'),
    path('user-churn-analysis/', views.UserChurnAnalysisView.as_view(), name='user_churn_analysis'),
]
