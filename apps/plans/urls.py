from django.urls import path
from django.urls import path
from . import views

app_name = 'plans'

urlpatterns = [
    path('', views.index, name='index'),
    path('input_rm/', views.input_rm, name='input_rm'),
    path('weekly_plan/', views.weekly_plan, name='weekly_plan'),
]