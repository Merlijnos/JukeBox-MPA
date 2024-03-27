from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, RegisterForm
from .models import Playlist, Song
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from .spotify import get_auth_token, get_playlist, get_track
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlparse, parse_qs

@login_required
def playlist_view(request):
    if request.method == 'POST':
        spotify_link = request.POST.get('spotify_link')
        parsed_link = urlparse(spotify_link)
        playlist_id = parsed_link.path.split('/')[-1]
        return HttpResponseRedirect(reverse('playlist_detail_view', args=[playlist_id]))
    else:
        return render(request, 'Mpapp/playlist.html')

class LogoutViewGet(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

@login_required
def home_view(request):
    auth_token = get_auth_token()
    playlists = get_playlist(request.user.username, auth_token)
    return render(request, 'Mpapp/home.html', {'playlists': playlists})

@login_required
def playlist_detail_view(request, playlist_id):
    auth_token = get_auth_token()
    playlist = get_playlist(playlist_id, auth_token)
    for song in playlist['tracks']['items']:
        # Access the album's images
        album_images = song['track']['album']['images']
        # Check if the album has images
        if album_images:
            # Get the URL of the first image
            image_url = album_images[0]['url']
            print(image_url)
    return render(request, 'Mpapp/playlist_detail.html', {'playlist': playlist})

@login_required
def all_songs(request):
    songs = Song.objects.all()
    return render(request, 'Mpapp/all_songs.html', {'songs': songs})

@login_required
def song_list(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    songs = Song.objects.filter(genre=genre)
    return render(request, 'Mpapp/songs.html', {'songs': songs})

@login_required
def song_detail(request, song_id):
    auth_token = get_auth_token()
    song = get_track(song_id, auth_token)
    return render(request, 'Mpapp/song_detail.html', {'song': song})

@login_required
def create_playlist(request):
    new_playlist = Playlist(name="My Playlist")
    new_playlist.save()

    song1 = Song(title="Song 1", artist="Artist 1")
    song1.save()
    song2 = Song(title="Song 2", artist="Artist 2")
    song2.save()

    new_playlist.songs.add(song1, song2)

    return redirect('playlist_detail_view', playlist_id=new_playlist.id)
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