from datetime import timedelta, timezone
from django.db.models import Sum, Avg
from .models import Conversion, Thread, Post, UserActivity, User

class UserActivityAlgorithm:
    @staticmethod
    def calculate_activity_score(user):
        """
        Calculate user engagement score based on various activities.
        """
        thread_count = Thread.objects.filter(creator=user).count()
        post_count = Post.objects.filter(creator=user).count()
        upvote_received_count = Post.objects.filter(thread__creator=user).aggregate(Sum('upvotes'))['upvotes__sum'] or 0
        conversion_count = Conversion.objects.filter(user=user).count()

        engagement_score = (
            thread_count * 10 +
            post_count * 5 +
            upvote_received_count * 2 +
            conversion_count * 20
        )

        return engagement_score

def calculate_sentiment(user):
    """
    Calculate sentiment score for a user (example function).
    """
    # Example sentiment analysis function
    # Replace with actual sentiment analysis logic
    return 0.5  # Example sentiment score

def calculate_popularity(user):
    """
    Calculate popularity score for a user's threads (example function).
    """
    # Example calculation based on thread views and upvotes
    return user.thread_set.aggregate(Sum('view_count'))['view_count__sum'] or 0

def calculate_average_post_length(user):
    """
    Calculate the average length of posts made by a user.
    """
    total_posts = Post.objects.filter(creator=user).count()
    total_post_length = Post.objects.filter(creator=user).aggregate(Sum('content_length'))['content_length__sum'] or 0

    if total_posts == 0:
        return 0
    return total_post_length / total_posts

def identify_inactive_users(days_threshold=30):
    """
    Identify inactive users who haven't interacted for a certain number of days.
    """
    active_users = UserActivity.objects.filter(timestamp__gte=timezone.now() - timedelta(days=days_threshold)).values('user')
    inactive_users = User.objects.exclude(id__in=active_users)
    return inactive_users

def calculate_thread_participation_ratio(user):
    """
    Calculate the thread participation ratio for a user.
    """
    total_threads_created = Thread.objects.filter(creator=user).count()
    total_posts_made = Post.objects.filter(creator=user).count()

    if total_threads_created == 0:
        return 0
    return total_posts_made / total_threads_created

# ... Add more algorithms as needed
