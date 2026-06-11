from django.shortcuts import render
from .forms import CarForm, ExpenseForm
from .models import Car, Expense, ExpenseCategory
from django.db.models import Sum, Count
import json
from django.db.models.functions import TruncMonth


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

    car_id = request.GET.get('car')
    category_id = request.GET.get('category')

    if car_id:
        expenses = expenses.filter(
            car_id=car_id
        )

    if category_id:
        expenses = expenses.filter(
            category_id=category_id
        )

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

    cars = Car.objects.all()

    categories = ExpenseCategory.objects.all()

    category_chart = (
        expenses
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    monthly_stats = (
        Expense.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('-month')[:3]
    )

    forecast = 0

    if monthly_stats:

        total_sum = 0

        for month in monthly_stats:
            total_sum += month['total']

        forecast = total_sum / len(monthly_stats)

    labels = []
    totals = []

    for item in category_chart:
        labels.append(item['category__name'])
        totals.append(float(item['total']))

    print(labels)
    print(totals)

    return render(
        request,
        'cars/expense_list.html',
        {
            'expenses': expenses,
            'total_amount': total_amount,
            'expense_count': expense_count,
            'top_category': top_category,
            'average_expense': average_expense,

            'cars': cars,
            'categories': categories,

            'selected_car': car_id,
            'selected_category': category_id,
            'chart_labels': json.dumps(labels),
            'chart_totals': json.dumps(totals),
            'forecast': round(forecast, 2),
        }
    )