from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.index, name='index'),
    path('recommend/', views.recommend_videos, name='recommend'),
    path('detail/<int:video_id>/', views.video_detail, name='detail'),
    path('like/<int:video_id>/', views.like_video, name='like'),
    path('save/<int:video_id>/', views.save_video, name='save'),
]