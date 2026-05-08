from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('cars/', views.car_list, name='car_list'),
    path('cars/add/', views.car_create, name='car_create'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('cars/<int:pk>/edit/', views.car_update, name='car_update'),
    path('cars/<int:pk>/delete/', views.car_delete, name='car_delete'),
]