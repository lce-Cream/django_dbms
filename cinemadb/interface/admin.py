from django.contrib import admin
from .models import *

@admin.register(Movie)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'ganre')


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('start', 'movie', 'hall')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('price', 'seat', 'owner', 'session')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


@admin.register(Worker)
class WorlerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'salary')