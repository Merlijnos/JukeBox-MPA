from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import register, home_view, login_view, logout_view, create_playlist, view_playlist, add_song, remove_song

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('playlist/', views.playlist_view, name='playlist_view'),
    path('all_playlists/', views.view_all_playlists, name='all_playlists'),
    path('playlist/<int:playlist_id>/delete/', views.delete_playlist, name='delete_playlist'),
    path('playlist_detail/<str:playlist_id>/', views.playlist_detail_view, name='playlist_detail_view'),
    path('create_playlist/', create_playlist, name='create_playlist'),
    path('playlist/<int:playlist_id>/', view_playlist, name='view_playlist'),
    path('playlist/<int:playlist_id>/add_song/', add_song, name='add_song'),
    path('playlist/<int:playlist_id>/remove_song/<int:song_id>/', views.remove_song, name='remove_song'),
]