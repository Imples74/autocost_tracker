from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('cars/', views.car_list, name='car_list'),
    path('cars/add/', views.car_create, name='car_create'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('cars/<int:pk>/edit/', views.car_update, name='car_update'),
    path('cars/<int:pk>/delete/', views.car_delete, name='car_delete'),
    path(
        'cars/<int:car_pk>/expenses/add/',
        views.expense_create_for_car,
        name='expense_create_for_car'
    ),

    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.expense_create, name='expense_create'),
    path('expenses/<int:pk>/edit/', views.expense_update, name='expense_update'),
    path('expenses/<int:pk>/delete/', views.expense_delete, name='expense_delete'),
]