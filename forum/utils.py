from django.db.models import Sum
from .models import Thread, Post, UserActivity, Conversion

def calculate_user_engagement(user):
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

def calculate_sentiment(post):
    """
    Calculate sentiment score for a post (example function).
    """
    # Example sentiment analysis function
    # Replace with actual sentiment analysis logic
    return 0.5  # Example sentiment score

def calculate_popularity(thread):
    """
    Calculate popularity score for a thread.
    """
    popularity_score = thread.view_count + thread.upvotes
    return popularity_score
