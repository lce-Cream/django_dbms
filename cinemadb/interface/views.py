from django.contrib import auth
from django.shortcuts import redirect, render
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Hall, Movie

def home(request):
    return render(request, 'interface/home.html', {'tab_title': 'cinemadb'})


@login_required(login_url='page.login')
def movies(request):
    movie_list = Movie.objects.all()
    return render(request, 'interface/movies.html', {'tab_title': 'movies', 'movie_list': movie_list})

@login_required(login_url='page.login')
def halls(request):
    hall_list = Hall.objects.all()
    return redirect(request, 'interface/halls.html', {'tab_title': 'halls', 'hall_list': hall_list})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user:
            print('+++++LOGIN SUCCESS')
            auth.login(request, user)
            return redirect('page.movies')
        else:
            print('++++ERRORO', username, password)
            print(request, request.POST)
            return render(request, 'interface/login.html', {'error': True})
    return render(request, 'interface/login.html')


def register(request):
    form = UserRegistrationForm()
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('page.home')
    return render(request, 'interface/registration.html', {'form': form})


@login_required(login_url='page.login')
def logout(request):
    auth.logout(request)
    return redirect('page.home')

