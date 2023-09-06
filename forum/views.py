import logging
from django.http import JsonResponse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import FormView
from django.contrib import messages
import requests
from .models import Category, Thread, Post, UserActivity, Conversion, UserFeedback
from .form import ThreadForm, PostForm, UserFeedbackForm, ReplyForm
from .utils import calculate_user_engagement, calculate_sentiment, calculate_popularity
from .algorithms import UserActivityAlgorithm, calculate_average_post_length, calculate_sentiment, calculate_popularity, calculate_thread_participation_ratio, identify_inactive_users

posts_per_page = 10


def forum_view(request):
    page = int(request.GET.get('page', 1))
    start_index = (page - 1) * posts_per_page
    end_index = start_index + posts_per_page

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

    # Create or get the "Home" thread and a default category
    default_category, _ = Category.objects.get_or_create(name="General")
    
    # Use the 'admin' user as the default creator (change 'admin' to the desired username)
    default_creator = User.objects.get(username='learnsync')

    home_thread, created = Thread.objects.get_or_create(
        title="Home",
        defaults={
            'category': default_category,
            'creator': default_creator,
        }
    )

    threads = Thread.objects.all()
    categories = Category.objects.all()

    # Check if a post has been liked
    if 'like_post_id' in request.GET:
        try:
            post_to_like = Post.objects.get(pk=request.GET['like_post_id'])
        except (ValueError, Post.DoesNotExist):
            post_to_like = None

        if post_to_like:
            # Check if the user has already liked the post
            if request.user in post_to_like.likes.all():
                messages.warning(request, 'You have already liked this post.')
            else:
                post_to_like.likes.add(request.user)
                messages.success(request, 'You have successfully liked the post.')

    # Check if a post has been unliked
    if 'unlike_post_id' in request.GET:
        try:
            post_to_unlike = Post.objects.get(pk=request.GET['unlike_post_id'])
        except (ValueError, Post.DoesNotExist):
            post_to_unlike = None

        if post_to_unlike:
            # Check if the user has already unliked the post
            if request.user not in post_to_unlike.likes.all():
                messages.warning(request, 'You have not liked this post.')
            else:
                post_to_unlike.likes.remove(request.user)
                messages.success(request, 'You have successfully unliked the post.')

    context = {
        'posts': posts,
        'threads': threads,
        'categories': categories,
        'create_thread_form': ThreadForm(),
        'create_post_form': PostForm(),
    }
    return render(request, 'forum/forum_two.html', context)


logger = logging.getLogger(__name__)


def create_post(request):
    if 'thread_id' in request.POST:
        try:
            thread = get_object_or_404(Thread, pk=request.POST['thread_id'])
        except ValueError:
            thread = None

        if thread:
            post_form = PostForm(request.POST)

            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.creator = request.user
                post.thread = thread
                if 'parent_post_id' in request.POST:
                    parent_post_id = request.POST['parent_post_id']
                    if parent_post_id:
                        try:
                            parent_post = Post.objects.get(pk=parent_post_id)
                            post.parent_post = parent_post
                        except Post.DoesNotExist:
                            # Log an error and show an error message
                            logger.error(f"Parent post with ID {parent_post_id} does not exist.")
                            messages.error(request, 'Error: Parent post does not exist.')

                post.save()
                messages.success(request, 'Post successfully created.')

    elif 'category' in request.POST:
        try:
            category = get_object_or_404(Category, pk=request.POST['category'])
        except ValueError:
            category = None

        if category:
            thread_form = ThreadForm(request.POST)

            if thread_form.is_valid():
                thread = thread_form.save(commit=False)
                thread.creator = request.user
                thread.category = category
                thread.save()
                messages.success(request, 'Thread successfully created.')

    return redirect('forum_two')
    
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