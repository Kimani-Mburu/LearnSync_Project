import logging
import os
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView

from django.shortcuts import render
from django.views.generic import ListView
from .models import ResearchPaper, ThesisPaper
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin



class IndexView(ListView):
    template_name = 'app/index.html'
    context_object_name = 'recent_papers'
    paginate_by = 10

    def get_queryset(self):
        research_papers = ResearchPaper.objects.all()
        thesis_papers = ThesisPaper.objects.all()
        return list(research_papers) + list(thesis_papers)


class SearchView(ListView):
    template_name = 'app/search_results.html'
    context_object_name = 'search_results'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('search')
        research_papers = ResearchPaper.objects.filter(title__icontains=query)
        thesis_papers = ThesisPaper.objects.filter(title__icontains=query)
        suggestions = list(research_papers.values('title')) + \
            list(thesis_papers.values('title'))
        self.suggestions = suggestions  # Store suggestions to use in get_context_data
        return list(research_papers) + list(thesis_papers)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('search')
        context['suggestions'] = self.suggestions
        # Pass the slug or ID of each paper in the search results to the context
        context['paper_slugs'] = [
            paper.slug for paper in context['search_results']]
        return context


def search_suggestions(request):
    query = request.GET.get('query')
    research_papers = ResearchPaper.objects.filter(
        title__icontains=query).values('title')
    thesis_papers = ThesisPaper.objects.filter(
        title__icontains=query).values('title')
    suggestions = list(research_papers) + list(thesis_papers)
    return JsonResponse(suggestions, safe=False)

class CombinedView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        paper = self.get_paper_by_slug(slug)

        if not paper:
            raise Http404("No paper found matching the given query.")

        # Increment the view count
        paper.increase_views()

        context = {
            'object': paper,
            'related_papers': self.get_related_papers(paper)
        }
        return render(request, 'app/detail_view.html', context)

    def get_paper_by_slug(self, slug):
        research_paper = ResearchPaper.objects.filter(slug=slug).first()
        if research_paper:
            return research_paper

        thesis_paper = ThesisPaper.objects.filter(slug=slug).first()
        if thesis_paper:
            return thesis_paper

        return None

    def get_related_papers(self, paper):
        # Implement the logic to get related papers based on tags and categories
        # For example:
        related_papers = paper.__class__.objects.filter(tags__in=paper.tags.all()).exclude(pk=paper.pk).distinct()[:3]
        return related_papers

    def post(self, request, *args, **kwargs):
        # Handle the file download request
        slug = kwargs['slug']
        paper = self.get_paper_by_slug(slug)

        if not paper:
            logging.error(f"Paper not found with slug: {slug}")
            raise Http404("Paper not found.")

        file_path = os.path.join(settings.MEDIA_ROOT, paper.file.name)

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Implement additional permission checks here if required
            # For example, you can check if the user is the owner of the paper or has specific permissions.

            try:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as file:
                        response = HttpResponse(file.read(), content_type='application/octet-stream')
                        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                        return response
                else:
                    logging.error(f"File not found at path: {file_path}")
                    raise Http404("File not found.")
            except Exception as e:
                logging.error(f"Error occurred during file download: {e}")
                raise Http404("An error occurred while downloading the file.")
        else:
            # Redirect to the login page if the user is not authenticated
            return redirect(reverse('login'))  # Assuming you have a URL pattern named 'login' for the login view
    
class DashboardView(View):
    def get(self, request):
        user_profile = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'cash_balance': 1000,
            'image': 'path/to/profile/image.jpg',
        }

        recent_activity = [
            {'activity': 'Uploaded paper: "Research Paper 1"',
                'timestamp': 'June 12, 2023 10:30 AM'},
            {'activity': 'Purchased paper: "Scientific Study"',
                'timestamp': 'June 10, 2023 2:45 PM'},
            {'activity': 'Uploaded paper: "Case Study 2"',
                'timestamp': 'June 9, 2023 9:15 AM'},
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
