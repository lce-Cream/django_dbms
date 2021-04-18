# from django.db.models import fields
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from django import forms
from .models import *


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'


class HallForm(ModelForm):
    class Meta:
        model = Hall
        fields = '__all__'


class SessionForm(ModelForm):
    class Meta:
        model = Session
        fields = '__all__'


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'