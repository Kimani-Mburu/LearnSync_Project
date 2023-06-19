from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(null=True,max_length=50)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/')
    social_site_urls = models.URLField(blank=True)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    INTEREST_CHOICES = [
        ('T', 'Technology'),
        ('S', 'Science'),
        ('E', 'Engineering'),
        ('M', 'Mathematics'),
        ('A', 'Arts'),
        ('O', 'Other'),
    ]
    interests = models.CharField(max_length=1, choices=INTEREST_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ThesisPaper(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    publication_date = models.DateField()
    document = models.FileField(upload_to='thesis_papers/')
    tags = models.ManyToManyField('Tag')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_papers', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('thesis-paper-detail', args=[str(self.slug)])

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save()

    def like_paper(self, user):
        self.likes.add(user)

    def unlike_paper(self, user):
        self.likes.remove(user)

    @property
    def total_likes(self):
        return self.likes.count()
    

class ResearchPaper(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    authors = models.ManyToManyField(UserProfile)
    abstract = models.TextField()
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    file = models.FileField(upload_to='research_papers/')
    published_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('research_paper_detail', kwargs={'slug': self.slug})
    

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='assignments/')
    uploaded_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title