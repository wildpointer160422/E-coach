from django.urls import path
from . import views

app_name = 'coach'

urlpatterns = [
    path('', views.index, name='index'),
    path('ai-coach-api', views.ai_coach_api, name='ai_coach_api'),
]