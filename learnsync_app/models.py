from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from docx import Document
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

import os
import io
import logging
from docx import Document
from docx2pdf import convert
from odf import text as odf_text
from odf import teletype
from odf.opendocument import load
from docx.opc.exceptions import PackageNotFoundError
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile

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

from django.db import models

class Reference(models.Model):
    research_paper = models.ForeignKey('learnsync_app.ResearchPaper', on_delete=models.CASCADE, related_name='research_references', blank=True, null=True)
    thesis_paper = models.ForeignKey('learnsync_app.ThesisPaper', on_delete=models.CASCADE, related_name='thesis_references', blank=True, null=True)
    content = models.TextField()

    def __str__(self):
        return self.content[:50]  # Display the first 50 characters of the content as the string representation
    
class ResearchPaper(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    authors = models.ManyToManyField('Author', related_name='research_papers')
    abstract = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    file = models.FileField(upload_to='research_papers/')
    references = models.ManyToManyField(Reference, blank=True, related_name='research_papers')
    citation = models.TextField(blank=True)
    views = models.PositiveIntegerField(default=0)
    publication_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.publication_date:
            self.publication_date = timezone.now().date()

        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('learnsync_app:paper_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save()

class Author(models.Model):
    full_name = models.CharField(max_length=255)
    affiliation = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name

class ThesisPaper(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    publication_date = models.DateField()
    document = models.FileField(upload_to='thesis_papers/')
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    views = models.PositiveIntegerField(default=0)
    references = models.ManyToManyField(Reference, blank=True, related_name='thesis_papers')
    citation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.publication_date:
            self.publication_date = timezone.now().date()

        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('learnsync_app:paper_detail', args=[str(self.slug)])

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save()