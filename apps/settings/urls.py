from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.index, name='index'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('update_goal/', views.update_goal, name='update_goal'),
    path('update_activity_level/', views.update_activity_level, name='update_activity_level'),
]