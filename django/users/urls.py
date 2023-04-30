from django.urls import path, include
from . import views

urlpatterns = [
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('auth/login', views.LoginUser.as_view(), name='login'),
    path('auth/logout', views.logout_user, name='logout'),
]