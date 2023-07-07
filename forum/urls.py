from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.forum, name='forum'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('category/<int:category_id>/create_thread/', views.create_thread, name='create_thread'),
    path('thread/<int:thread_id>/reply/', views.reply_to_thread, name='reply_to_thread'),
]
