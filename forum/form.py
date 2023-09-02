from django import forms
from .models import Reply, Thread, Post, UserFeedback

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'category']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']  # Adjust this based on your actual field names

    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control mb-2', 'rows': '4', 'placeholder': 'Write a post'}),
    )

class UserFeedbackForm(forms.ModelForm):
    class Meta:
        model = UserFeedback
        fields = ['feedback']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']