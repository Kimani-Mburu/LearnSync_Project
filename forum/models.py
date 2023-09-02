from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    thread_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Thread(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)
    upvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    parent_post = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)
    upvotes = models.PositiveIntegerField(default=0)
    sentiment_score = models.FloatField(default=0.0)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Post by {self.creator.username}"

    def calculate_replies(self):
        """
        Calculate the number of replies to this post.
        """
        return Post.objects.filter(parent_post=self).count()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def increase_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def increase_likes(self):
        self.likes += 1
        self.save(update_fields=['likes'])

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reply by {self.creator.username}"

class Conversion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversion_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
