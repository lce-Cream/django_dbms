from django.urls import path
from .views import *

urlpatterns = [
    path(route='', view=home, name='page.home'),
    path('register', view=register, name='page.register'),
    path('login', view=login, name='page.login'),
    path('logout', view=logout, name='page.logout'),
    path('movies', view=movies, name='page.movies'),
    # path('delete/<str:table>/<int:id>/', view=delete, name='lab5.delete'),
    # path('add', view=add, name='lab5.add'),
    # path('count', view=count, name='lab5.count'),
    # path('department', view=department, name='lab5.department'),
]
