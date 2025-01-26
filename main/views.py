from django.shortcuts import render, get_object_or_404, redirect
from .models import Song, Playlist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    songs = Song.objects.all()
    play_song_id = request.GET.get('play', None)
    play_song = None
    playlists = Playlist.objects.filter(user=request.user)

    if request.method == "POST":
        song_id = request.POST.get('song_id')
        playlist_id = request.POST.get('playlist_id')

        if song_id and playlist_id:
            playlist = Playlist.objects.get(id=playlist_id, user=request.user)
            song = Song.objects.get(id=song_id)
            playlist.song.add(song)

    if play_song_id:
        play_song = get_object_or_404(Song, id=play_song_id)

    return render(request, 'main/index.html', {'songs': songs, 'play_song': play_song, 'playlists': playlists})

def register_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password != password2:
            print("Passwords didn't match!")
            return redirect('register_user')

        if User.objects.filter(username=username).exists():
            print("Username already taken!")
            return redirect('register_user')

        try:
            user = User.objects.create(username=username, password=password)
            user.save()
            login(request, user)
            print("Successfully registered!!!")
            return redirect('index')
        except Exception as e:
            print(f"Error: {e}")
            return redirect('register_user')

    return render(request, 'main/register_user.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Successfully logged in!!!")
            return redirect('index')
        else:
            print("Wrong credentions")
            return redirect('login_user')

    return render(request, 'main/login_user.html')

def logout_user(request):
    logout(request)
    print("Successfully logged out!!!")
    return redirect('index')

def create_playlist(request):
    if request.method == "POST":
        name_playlist = request.POST.get("name-playlist")

        if request.user.is_authenticated:
            create_playlist = Playlist.objects.create(name=name_playlist, user=request.user)
            create_playlist.save()
            return redirect("index")

        else:
            return redirect('index')
        
    return render(request, 'main/create_playlist.html')

def view_playlist(request, pk):
    if request.user.is_authenticated:
        playlist = Playlist.objects.get(id=pk, user=request.user)
        return render(request, 'main/view_playlist.html', {"playlist": playlist})
    
    else:
        return redirect('index')
        
def all_playlists(request):
    if request.user.is_authenticated:
        playlists = Playlist.objects.filter(user=request.user)
        return render(request, 'main/all_playlists.html', {"playlists": playlists})

    else:
        return redirect('index')
