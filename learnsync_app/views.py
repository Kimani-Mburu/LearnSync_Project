from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, DetailView

class HomeView(TemplateView):
    template_name = 'app/index.html'

class Detail(TemplateView):
    template_name = 'app/detail_view.html'

class DashboardView(View):
    def get(self, request):
        user_profile = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'cash_balance': 1000,
            'image': 'path/to/profile/image.jpg',
        }

        recent_activity = [
            {'activity': 'Uploaded paper: "Research Paper 1"', 'timestamp': 'June 12, 2023 10:30 AM'},
            {'activity': 'Purchased paper: "Scientific Study"', 'timestamp': 'June 10, 2023 2:45 PM'},
            {'activity': 'Uploaded paper: "Case Study 2"', 'timestamp': 'June 9, 2023 9:15 AM'},
        ]

        usage_statistics = {
            'total_uploaded': 10,
            'total_purchased': 5,
        }

        progress = 75

        context = {
            'user_profile': user_profile,
            'recent_activity': recent_activity,
            'usage_statistics': usage_statistics,
            'progress': progress,
        }

        return render(request, 'dashboard.html', context)