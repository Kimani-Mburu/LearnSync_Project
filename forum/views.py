from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Thread, Post
from .form import ThreadForm, PostForm

@login_required
def forum(request):
    categories = Category.objects.all()
    return render(request, 'forum/forum.html', {'categories': categories})

@login_required
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    threads = Thread.objects.filter(category=category)
    return render(request, 'forum/category_detail.html', {'category': category, 'threads': threads})

@login_required
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = Post.objects.filter(thread=thread)
    return render(request, 'forum/thread_detail.html', {'thread': thread, 'posts': posts})

@login_required
def create_thread(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.category = category
            thread.created_by = request.user
            thread.save()
            return redirect('forum:category_detail', category_id=category.id)
    else:
        form = ThreadForm()
    return render(request, 'forum/create_thread.html', {'category': category, 'form': form})

@login_required
def reply_to_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.created_by = request.user
            post.save()
            return redirect('forum:thread_detail', thread_id=thread.id)
    else:
        form = PostForm()
    return render(request, 'forum/reply_to_thread.html', {'thread': thread, 'form': form})
