from django.urls import path
from . import views

app_name = 'plans'

urlpatterns = [
    path('', views.index, name='index'),
    path('input_rm/', views.input_rm, name='input_rm'),
    path('weekly_plan/', views.weekly_plan, name='weekly_plan'),
    path('ai_generator/', views.ai_generator_view, name='ai_generator'),
    path('generate_plan/', views.generate_plan, name='generate_plan'),
    path('ai_weekly_plan/', views.ai_weekly_plan, name='ai_weekly_plan'),
]
