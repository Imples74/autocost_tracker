from django.urls import path
from .views import home, car_create, car_list
from .views import (
    home,
    car_create,
    car_list,
    expense_create,
    expense_list,
    car_update,
    car_delete,
)

path(
    'expenses/',
    expense_list,
    name='expense_list'
),

path(
    'expenses/create/',
    expense_create,
    name='expense_create'
),

urlpatterns = [
    path('', home, name='home'),

    path('cars/', car_list, name='car_list'),
    path('cars/create/', car_create, name='car_create'),

    path('expenses/', expense_list, name='expense_list'),
    path('expenses/create/', expense_create, name='expense_create'),

    path(
    'cars/<int:pk>/edit/',
    car_update,
    name='car_update'
),

path(
    'cars/<int:pk>/delete/',
    car_delete,
    name='car_delete'
),
]