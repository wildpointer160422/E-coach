from django.urls import path
from . import views

app_name = 'nutrition'

urlpatterns = [
    path('', views.index, name='index'),
    path('statics/', views.statics, name='statics'),
    path('record-strength/', views.record_strength, name='record_strength'),
    path('record-cardio/', views.record_cardio, name='record_cardio'),
    path('record-nutrition/', views.record_nutrition, name='record_nutrition'),
    path('record-water/', views.record_water, name='record_water'),
    path('get-bmr/', views.get_bmr, name='get_bmr'),
]