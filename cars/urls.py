from django.urls import path
from .views import home, car_create, car_list

urlpatterns = [
    path('', home, name='home'),

    path(
        'cars/',
        car_list,
        name='car_list'
    ),

    path(
        'cars/create/',
        car_create,
        name='car_create'
    ),
]