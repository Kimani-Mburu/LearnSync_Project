from django.http import JsonResponse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
import requests
from .models import Category, Thread, Post, UserActivity, Conversion, UserFeedback
from .form import ThreadForm, PostForm, UserFeedbackForm, ReplyForm
from .utils import calculate_user_engagement, calculate_sentiment, calculate_popularity
from .algorithms import UserActivityAlgorithm, calculate_average_post_length, calculate_sentiment, calculate_popularity, calculate_thread_participation_ratio, identify_inactive_users

class ForumView(View):
    template_name = 'forum/forum_two.html'
    posts_per_page = 10

    def get(self, request, *args, **kwargs):
        page = int(request.GET.get('page', 1))
        start_index = (page - 1) * self.posts_per_page
        end_index = start_index + self.posts_per_page

        posts = Post.objects.order_by('-created_at')[start_index:end_index]

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            posts_data = [
                {
                    'id': post.id,
                    'content': post.content,
                    'creator': post.creator.username,
                    'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
                for post in posts
            ]
            return JsonResponse({'posts': posts_data})

        threads = Thread.objects.all()
        categories = Category.objects.all()
        context = {
            'posts': posts,
            'threads': threads,
            'categories': categories,
            'create_thread_form': ThreadForm(),
            'create_post_form': PostForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        thread_id = request.POST.get('thread_id')  # Get the thread_id from the form data
        
        post_form = PostForm(request.POST)  # Assuming you're using PostForm for creating posts
        
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.creator = request.user
            post.thread_id = thread_id
            if 'parent_post_id' in request.POST:
                post.parent_post_id = request.POST.get('parent_post_id')
            post.save()

        return redirect('forum_two')  # Redirect back to the forum page
    
    
class UserFeedbackFormView(FormView):
    """
    Provide a form for users to submit feedback.
    """
    template_name = 'forum/user_feedback.html'
    form_class = UserFeedbackForm
    success_url = '/thank-you/'  # Redirect to a thank you page after form submission

    def form_valid(self, form):
        feedback = form.cleaned_data['feedback']
        UserFeedback.objects.create(user=self.request.user, feedback=feedback)

        return super().form_valid(form)

class UserConversionView(ListView):
    """
    Display a list of user conversions with timestamps and types.
    """
    model = Conversion
    template_name = 'forum/user_conversion.html'
    context_object_name = 'conversions'



class SearchResultsView(ListView):
    """
    Display search results based on user queries, showing relevant threads and posts.
    """
    template_name = 'forum/search_results.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            threads = Thread.objects.filter(title__icontains=query)
            posts = Post.objects.filter(content__icontains=query)
            return list(threads) + list(posts)
        return []
class AnalyticsDashboardView(ListView):
    """
    Create an analytics dashboard for administrators to view and analyze metrics.
    """
    template_name = 'forum/analytics_dashboard.html'
    context_object_name = 'analytics_data'

    def get_queryset(self):
        user = self.request.user

        user_engagement = UserActivityAlgorithm.calculate_activity_score(user)
        thread_activity = Thread.objects.all().count()
        post_activity = Post.objects.all().count()
        sentiment_score = calculate_sentiment(user)
        popularity_score = calculate_popularity(user)
        average_post_length = calculate_average_post_length(user)
        inactive_users = identify_inactive_users(days_threshold=30)
        thread_participation_ratio = calculate_thread_participation_ratio(user)

        return {
            'user_engagement': user_engagement,
            'thread_activity': thread_activity,
            'post_activity': post_activity,
            'sentiment_score': sentiment_score,
            'popularity_score': popularity_score,
            'average_post_length': average_post_length,
            'inactive_users': inactive_users,
            'thread_participation_ratio': thread_participation_ratio,
            # ... Include more metrics in the dictionary
        }
class TrendingThreadsView(ListView):
    """
    Display a list of threads sorted by popularity score (view counts + upvotes).
    """
    model = Thread
    template_name = 'forum/trending_threads.html'
    context_object_name = 'trending_threads'

    def get_queryset(self):
        return Thread.objects.all().order_by('-popularity_score')  # Assuming you have a popularity_score field

class SentimentAnalysisView(ListView):
    """
    Display sentiment analysis scores for posts and allow filtering by sentiment.
    """
    model = Post
    template_name = 'forum/sentiment_analysis.html'
    context_object_name = 'posts'

    def get_queryset(self):
        sentiment_filter = self.request.GET.get('sentiment')
        if sentiment_filter:
            return Post.objects.filter(sentiment__gte=float(sentiment_filter))
        return Post.objects.all()

class UserChurnAnalysisView(ListView):
    """
    Identify inactive users and suggest re-engagement strategies.
    """
    template_name = 'forum/user_churn_analysis.html'
    context_object_name = 'inactive_users'

    def get_queryset(self):
        # Implement logic to identify inactive users and provide suggestions
        return []