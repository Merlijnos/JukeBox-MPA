from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import register, home_view, login_view, logout_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('songs/<str:song_id>/', views.song_detail, name='song_detail'),
    path('song_detail/', views.all_songs, name='all_songs'),
    path('playlist/', views.playlist_view, name='playlist_view'),
    path('playlist_detail/<str:playlist_id>/', views.playlist_detail_view, name='playlist_detail_view'),
    path('create_playlist/', views.create_playlist, name='create_playlist'),
]