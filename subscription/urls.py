from django.urls import path
from . import views

app_name = 'subscription'

urlpatterns = [
    path('subscription-plans/', views.SubscriptionPlanListView.as_view(), name='subscription_plan_list'),
    path('subscription-plan/<int:pk>/', views.SubscriptionPlanDetailView.as_view(), name='subscription_plan_detail'),
]
