from . import views
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home , name='home'),
    path('chat/', views.chat, name='chat'),
    path('login/', views.login , name='login'),
    path('logout/',views.user_logout, name="logout"),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('view_profile/<int:id>', views.view_profile, name='view_profile'),
    path('search_user/', views.search_user, name='search_user'),
    path('follow/<int:id>',views.follow ,name='follow'),
    path('unfollow/<int:id>',views.unfollow ,name='unfollow'),
]
