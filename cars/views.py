from django.shortcuts import render
from .forms import CarForm
from .models import Car
from .forms import CarForm, ExpenseForm
from .models import Car, Expense

def home(request):
    return render(request, 'home.html')

from django.shortcuts import redirect

def car_create(request):

    if request.method == 'POST':

        form = CarForm(request.POST)

        if form.is_valid():

            car = form.save(commit=False)

            car.owner = request.user

            car.save()

            return redirect('/cars/')

    else:

        form = CarForm()

    return render(
        request,
        'cars/car_form.html',
        {
            'form': form
        }
    )

def car_list(request):

    cars = Car.objects.all()

    return render(
        request,
        'cars/car_list.html',
        {
            'cars': cars
        }
    )

def expense_create(request):

    if request.method == 'POST':

        form = ExpenseForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('/expenses/')

    else:

        form = ExpenseForm()

    return render(
        request,
        'cars/expense_form.html',
        {
            'form': form
        }
    )

def expense_list(request):

    expenses = Expense.objects.all()

    return render(
        request,
        'cars/expense_list.html',
        {
            'expenses': expenses
        }
    )