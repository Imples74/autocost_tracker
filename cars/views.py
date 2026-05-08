from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CarForm
from .models import Car


def home(request):
    return render(request, 'home.html')


@login_required
def car_list(request):
    cars = Car.objects.filter(user=request.user)

    return render(request, 'cars/car_list.html', {
        'cars': cars,
    })


@login_required
def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST)

        if form.is_valid():
            car = form.save(commit=False)
            car.user = request.user
            car.save()
            return redirect('car_detail', pk=car.pk)
    else:
        form = CarForm()

    return render(request, 'cars/car_form.html', {
        'form': form,
        'title': 'Добавить автомобиль',
        'button_text': 'Добавить',
    })


@login_required
def car_detail(request, pk):
    car = get_object_or_404(
        Car,
        pk=pk,
        user=request.user
    )

    expenses = car.expenses.select_related('category')[:5]

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'expenses': expenses,
    })


@login_required
def car_update(request, pk):
    car = get_object_or_404(
        Car,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)

        if form.is_valid():
            form.save()
            return redirect('car_detail', pk=car.pk)
    else:
        form = CarForm(instance=car)

    return render(request, 'cars/car_form.html', {
        'form': form,
        'title': 'Редактировать автомобиль',
        'button_text': 'Сохранить',
    })


@login_required
def car_delete(request, pk):
    car = get_object_or_404(
        Car,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        car.delete()
        return redirect('car_list')

    return render(request, 'cars/car_confirm_delete.html', {
        'car': car,
    })