from django import forms
from .models import Reply, Thread, Post, UserFeedback

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'category']

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['thread_id', 'content']

    thread_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'class': 'hidden-input'}),  # Apply a custom CSS class
        required=False
    )

    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control post-content',
            'rows': '4',
            'placeholder': 'Write a post',
            'style': 'border: 1px solid #ccc; border-radius: 5px; padding: 10px; font-size: 16px;'
        }),
    )
    

class UserFeedbackForm(forms.ModelForm):
    class Meta:
        model = UserFeedback
        fields = ['feedback']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']