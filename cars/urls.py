from django.urls import path
from .views import home, car_create

urlpatterns = [
    path('', home, name='home'),

    path(
        'cars/create/',
        car_create,
        name='car_create'
    ),
]