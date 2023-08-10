from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import SubscriptionPlan

class SubscriptionPlanListView(View):
    def get(self, request):
        subscription_plans = SubscriptionPlan.objects.all()
        context = {'subscription_plans': subscription_plans}
        return render(request, 'subscription/plans.html', context)

class SubscriptionPlanDetailView(View):
    def get(self, request, pk):
        subscription_plan = get_object_or_404(SubscriptionPlan, pk=pk)
        context = {'subscription_plan': subscription_plan}
        return render(request, 'subscription/plan_detail.html', context)
