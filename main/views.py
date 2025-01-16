from django.shortcuts import render, get_object_or_404, redirect
from .models import Song
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    songs = Song.objects.all()
    play_song_id = request.GET.get('play', None)
    play_song = None

    if play_song_id:
        play_song = get_object_or_404(Song, id=play_song_id)

    return render(request, 'main/index.html', {'songs': songs, 'play_song': play_song})

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
