from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]