from django.urls import path
from .views import *

urlpatterns = [
    path(route='', view=home, name='interface.home'),
    # path('delete/<int:id>/', view=delete, name='lab5.delete'),
    # path('add', view=add, name='lab5.add'),
    # path('count', view=count, name='lab5.count'),
    # path('department', view=department, name='lab5.department'),
]
