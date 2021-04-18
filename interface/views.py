from django.contrib import auth
from django.shortcuts import redirect, render
from .forms import HallForm, MovieForm, SessionForm, TicketForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Hall, Movie, Session, Ticket

def home(request):
    return render(request, 'interface/home.html', {'tab_title': 'cinemadb'})


# tabels #
@login_required(login_url='page.login')
def movies(request):
    movie_list = Movie.objects.all()
    return render(request, 'interface/movies.html', {'tab_title': 'movies', 'movie_list': movie_list})


@login_required(login_url='page.login')
def halls(request):
    hall_list = Hall.objects.all()
    return render(request, 'interface/halls.html', {'tab_title': 'halls', 'hall_list': hall_list})


@login_required(login_url='page.login')
def sessions(request):
    session_list = Session.objects.all()
    return render(request, 'interface/sessions.html', {'tab_title': 'sessions', 'session_list': session_list})


@login_required(login_url='page.login')
def tickets(request):
    ticket_list = Ticket.objects.all()
    return render(request, 'interface/tickets.html', {'tab_title': 'tickets', 'ticket_list': ticket_list})


# edit, delete, add, search #
@login_required(login_url='page.login')
def edit(request, table, id):
    tables = {'movies': Movie, 'sessions': Session, 'halls': Hall, 'tickets': Ticket}
    forms = {'movies': MovieForm, 'sessions': SessionForm, 'halls': HallForm, 'tickets': TicketForm}
    record = tables[table].objects.get(id=id)
    form = forms[table](request.POST or None, instance=record)

    if form.is_valid():
        form.save()
        return redirect(f'page.{table}')
    return render(request, 'interface/edit.html', {'form': form})


@login_required(login_url='page.login')
def delete(request, table, id):
    tables = {'movies': Movie, 'sessions': Session, 'halls': Hall, 'tickets': Ticket}
    tables[table].objects.get(id=id).delete()
    return redirect(f'page.{table}')


@login_required(login_url='page.login')
def add(request, table):
    forms = {'movies': MovieForm, 'sessions': SessionForm, 'halls': HallForm, 'tickets': TicketForm}
    form = forms[table](request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(f'page.{table}')
    return render(request, 'interface/add.html', {'form': form})


@login_required(login_url='page.login')
def search(request, table):
    def movie_search():
        #it's a bit tricky one I came up with, kwargs are passed in filter if they aren't empty only
        #thus all this bloated 'if elif' stuff can be avoided, but it still looks kinda messy and repeated
        id, name, ganre = (request.GET[field] or '' for field in ('id', 'name', 'ganre'))
        keys = {'id': id, 'name__icontains': name, 'ganre__icontains': ganre}
        kwargs = {key: value for key, value in keys.items() if value}
        orderby = request.GET['orderby']
        movie_list = Movie.objects.filter(**kwargs).order_by(orderby)

        return render(request, f'interface/{table}.html',
        		      {'movie_list': movie_list, 'id': id, 'name': name, 'ganre': ganre, 'orderby': orderby})

    def session_search():
        id, start, movie, hall = (request.GET[field] or '' for field in ('id', 'start', 'movie', 'hall'))
        keys = {'id': id, 'start__lt': start, 'movie__name__icontains': movie, 'hall__name__icontains': hall}
        kwargs = {key: value for key, value in keys.items() if value}
        orderby = request.GET['orderby']
        session_list = Session.objects.filter(**kwargs).order_by(orderby)

        return render(request, f'interface/{table}.html',
        			  {'session_list': session_list, 'id': id, 'start': start, 'movie': movie, 'hall': hall, 'orderby': orderby})

    def hall_search():
        id, name, capacity = (request.GET[field] or '' for field in ('id', 'name', 'capacity'))
        keys = {'id': id, 'name__icontains': name, 'capacity__lt': capacity}
        kwargs = {key: value for key, value in keys.items() if value}
        orderby = request.GET['orderby']
        hall_list = Hall.objects.filter(**kwargs).order_by(orderby)

        return render(request, f'interface/{table}.html',
                      {'hall_list': hall_list, 'id': id, 'name': name, 'capacity': capacity, 'orderby': orderby})

    def ticket_search():
        id, price, seat, owner, session = (request.GET[field] or '' for field in ('id', 'price', 'seat', 'owner', 'session'))
        keys = {'id': id, 'price__lt': price, 'seat': seat, 'owner__name': owner, 'session': session}
        kwargs = {key: value for key, value in keys.items() if value}
        orderby = request.GET['orderby']
        ticket_list = Ticket.objects.filter(**kwargs).order_by(orderby)

        return render(request, f'interface/{table}.html',
                      {'ticket_list': ticket_list, 'id': id, 'price': price, 'seat': seat, 'owner': owner,
                       'session': session, 'orderby': orderby})

    tables = {'movies': movie_search, 'sessions': session_search, 'halls': hall_search, 'tickets': ticket_search}
    return tables[table]()

#log in, register, log out #
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('page.movies')
        else:
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

