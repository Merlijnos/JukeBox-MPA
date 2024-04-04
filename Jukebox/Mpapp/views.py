from urllib.parse import urlparse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import CustomPlaylist, Mpapp_song
from .forms import LoginForm, RegisterForm
from .spotify import get_auth_token, get_playlist, get_track


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home_view(request):
    auth_token = get_auth_token()
    playlists = get_playlist(request.user.username, auth_token)
    return render(request, 'Mpapp/home.html', {'playlists': playlists})

@login_required(login_url='login')
def view_all_playlists(request):
    playlists = CustomPlaylist.objects.all()
    return render(request, 'Mpapp/all_playlists.html', {'playlists': playlists})

@login_required(login_url='login')
def delete_playlist(request, playlist_id):
    playlist = CustomPlaylist.objects.get(id=playlist_id)
    if request.user == playlist.user:
        playlist.delete()
    return redirect('all_playlists')

@login_required(login_url='login')
def playlist_view(request):
    if request.method == 'POST':
        spotify_link = request.POST.get('spotify_link')
        parsed_link = urlparse(spotify_link)
        playlist_id = parsed_link.path.split('/')[-1]
        return HttpResponseRedirect(reverse('playlist_detail_view', args=[playlist_id]))
    else:
        return render(request, 'Mpapp/playlist.html')


@login_required(login_url='login')
def playlist_detail_view(request, playlist_id):
    auth_token = get_auth_token()
    playlist = get_playlist(playlist_id, auth_token)
    total_duration = 0
    for song in playlist['tracks']['items']:
        # Access the album's images
        album_images = song['track']['album']['images']
        # Check if the album has images
        if album_images:
            # Get the URL of the first image
            image_url = album_images[0]['url']
            print(image_url)
        # Add the duration of the song to the total duration
        total_duration += song['track']['duration_ms']
    # Convert total_duration from milliseconds to minutes and seconds
    total_duration = total_duration // 60000, (total_duration % 60000) // 1000
    return render(request, 'Mpapp/playlist_detail.html', {'playlist': playlist, 'total_duration': total_duration})

@login_required(login_url='login')
def create_playlist(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        spotify_ids = request.POST.getlist('spotify_ids')  # Get list of Spotify song IDs from the form
        playlist = CustomPlaylist.objects.create(name=name, user=request.user)
        auth_token = get_auth_token()
        for spotify_id in spotify_ids:
            track_data = get_track(spotify_id, auth_token)
            song, created = Mpapp_song.objects.get_or_create(
                spotify_id=spotify_id,
                defaults={
                    'title': track_data['name'],
                    'artist': track_data['artists'][0]['name']
                }
            )
            playlist.songs.add(song)  # Add the song to the playlist
        return redirect('view_playlist', playlist_id=playlist.id)  # Redirect to view_playlist view
    return render(request, 'Mpapp/create_playlist.html')

@login_required(login_url='login')
def view_playlist(request, playlist_id):
    playlist = CustomPlaylist.objects.get(id=playlist_id)
    if request.method == 'POST':
        spotify_id = request.POST.get('spotify_id')
        auth_token = get_auth_token()
        track_data = get_track(spotify_id, auth_token)
        song, created = Mpapp_song.objects.get_or_create(
            spotify_id=spotify_id,
            defaults={
                'title': track_data['name'],
                'artist': track_data['artists'][0]['name']
            }
        )
        playlist.songs.add(song)
        return redirect('view_playlist', playlist_id=playlist.id)
    return render(request, 'Mpapp/view_playlist.html', {'playlist': playlist})

@login_required(login_url='login')
def add_song(request, playlist_id):
    if request.method == 'POST':
        spotify_id = request.POST.get('spotify_id')
        auth_token = get_auth_token()
        track_data = get_track(spotify_id, auth_token)
        song, created = Mpapp_song.objects.get_or_create(
            spotify_id=spotify_id,
            defaults={
                'title': track_data['name'],
                'artist': track_data['artists'][0]['name']
            }
        )
        playlist = CustomPlaylist.objects.get(id=playlist_id)
        playlist.songs.add(song)
        return redirect('view_playlist', playlist_id=playlist.id)
    return render(request, 'Mpapp/add_song.html')

@login_required(login_url='login')
def remove_song(request, playlist_id, song_id):
    playlist = CustomPlaylist.objects.get(id=playlist_id)
    song = Mpapp_song.objects.get(id=song_id)
    playlist.songs.remove(song)
    return redirect('view_playlist', playlist_id=playlist.id)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'Mpapp/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'Mpapp/register.html', {'form': form})
