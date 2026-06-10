from django.shortcuts import render
from .forms import CarForm
from .models import Car
from .forms import CarForm, ExpenseForm
from .models import Car, Expense
from django.db.models import Sum, Count


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

    total_amount = (
        expenses.aggregate(
            total=Sum('amount')
        )['total']
        or 0
    )

    expense_count = expenses.count()

    category_stats = (
        Expense.objects
        .values('category__name')
        .annotate(
            total=Sum('amount')
        )
        .order_by('-total')
    )

    top_category = None

    if category_stats:
        top_category = category_stats[0]

    average_expense = 0

    if expense_count:
        average_expense = (
            total_amount /
            expense_count
        )

    return render(
        request,
        'cars/expense_list.html',
        {
            'expenses': expenses,
            'total_amount': total_amount,
            'expense_count': expense_count,
            'top_category': top_category,
            'average_expense': average_expense,
        }
    )