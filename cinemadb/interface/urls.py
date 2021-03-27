from django.urls import path
from .views import *

urlpatterns = [
    path('', view=home, name='page.home'),
    path('register', view=register, name='page.register'),
    path('login', view=login, name='page.login'),
    path('logout', view=logout, name='page.logout'),
    #tables
    path('movies', view=movies, name='page.movies'),
    path('halls', view=halls, name='page.halls'),
    path('sessions', view=sessions, name='page.sessions'),
    path('tickets', view=tickets, name='page.tickets'),
    #edit, delete, add, search
    path('edit/<str:table>/<int:id>/', view=edit, name='page.edit'),
    path('delete/<str:table>/<int:id>/', view=delete, name='page.delete'),
    path('add/<str:table>/', view=add, name='page.add'),
    path('search/<str:table>/', view=search, name='page.search'),

]
