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
        id, name, duration, ganre = (request.GET[field] or '' for field in ('id', 'name', 'duration', 'ganre'))
        movie_list = Movie.objects.all()

        if id:
            movie_list = movie_list.filter(id=id)
        elif name:
            movie_list = movie_list.filter(name__icontains=name)
        elif duration:
            movie_list = movie_list.filter(duration__lt=duration)
        elif ganre:
            movie_list = movie_list.filter(ganre__icontains=ganre)

        return render(request, f'interface/{table}.html',
        {'movie_list': movie_list, 'id': id, 'name': name, 'duration': duration, 'ganre': ganre})

    def session_search():
        id, start, movie, hall = (request.GET[field] or '' for field in ('id', 'start', 'movie', 'hall'))
        session_list = Session.objects.all()

        if id:
            session_list = session_list.filter(id=id)
        elif start:
            session_list = session_list.filter(start__lt=start)
        elif movie:
            session_list = session_list.filter(movie=movie)
        elif hall:
            session_list = session_list.filter(hall=hall)
        return render(request, f'interface/{table}.html',
        {'session_list': session_list, 'id': id, 'start': start, 'movie': movie, 'hall': hall})

    def hall_search():
        id = request.GET['id'] or None
        name = request.GET['name'] or ''
        capacity = request.GET['capacity'] or None
        hall_list = Hall.objects.all()

        if id:
            hall_list = hall_list.filter(id=id)
        elif name:
            hall_list = hall_list.filter(name__icontains=name)
        elif capacity:
            hall_list = hall_list.filter(capacity__lt=capacity)
        return render(request, f'interface/{table}.html',
        {'hall_list': hall_list, 'id': id, 'name': name, 'capacity': capacity})

    def ticket_search():
        id = request.GET['id'] or None
        price = request.GET['price'] or None
        seat = request.GET['seat'] or None
        owner = request.GET['owner'] or ''
        session = request.GET['session'] or ''
        ticket_list = Ticket.objects.all()

        if id:
            ticket_list = ticket_list.filter(id=id)
        elif price:
            ticket_list = ticket_list.filter(price=price)
        elif seat:
            ticket_list = ticket_list.filter(seat=seat)
        elif owner:
            ticket_list = ticket_list.filter(owner=owner)
        elif session:
            ticket_list = ticket_list.filter(session=session)
        return render(request, f'interface/{table}.html',
        {'ticket_list': ticket_list, 'id': id, 'price': price, 'seat': seat, 'owner': owner, 'session': session})

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

