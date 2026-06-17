from django.shortcuts import render
from .forms import CarForm, ExpenseForm
from .models import Car, Expense, ExpenseCategory
from django.db.models import Sum, Count
import json
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Sum

@login_required
def home(request):

    if request.user.is_authenticated:

        cars_count = (
            Car.objects.filter(
                owner=request.user
            ).count()
        )

        expenses = Expense.objects.filter(
            car__owner=request.user
        )

        expenses_count = expenses.count()

        total_expenses = (
            expenses.aggregate(
                total=Sum('amount')
            )['total']
            or 0
        )

    else:

        cars_count = 0
        expenses_count = 0
        total_expenses = 0

    return render(
        request,
        'home.html',
        {
            'cars_count': cars_count,
            'expenses_count': expenses_count,
            'total_expenses': total_expenses,
        }
    )

from django.shortcuts import redirect

@login_required
def car_create(request):

    if request.method == 'POST':
        form = CarForm(request.POST)

        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()

            return redirect('car_list')

    else:
        form = CarForm()

    return render(
        request,
        'cars/car_form.html',
        {'form': form}
    )

@login_required
def car_list(request):

    cars = Car.objects.filter(
        owner=request.user
    )

    search = request.GET.get(
        'search'
    )

    if search:

        cars = cars.filter(
            brand__icontains=search
        )

    sort = request.GET.get(
        'sort'
    )

    if sort == 'brand':
        cars = cars.order_by(
            'brand'
        )

    elif sort == 'year':
        cars = cars.order_by(
            '-year'
        )

    elif sort == 'mileage':
        cars = cars.order_by(
            '-mileage'
        )

    return render(
        request,
        'cars/car_list.html',
        {
            'cars': cars,
            'search': search,
            'sort': sort,
        }
    )

@login_required
def expense_create(request):

    if request.method == 'POST':

        form = ExpenseForm(request.POST)
        form.fields['car'].queryset = (
            Car.objects.filter(
                owner=request.user
            )
        )

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

@login_required
def expense_list(request):

    expenses = Expense.objects.filter(
        car__owner=request.user
    )

    car_id = request.GET.get('car')
    category_id = request.GET.get('category')

    sort = request.GET.get(
        'sort'
    )

    print("SORT =", sort)
    print(expenses.query)

    if car_id:
        expenses = expenses.filter(
            car_id=car_id
        )

    if category_id:
        expenses = expenses.filter(
            category_id=category_id
        )

    if sort == 'date':
        expenses = expenses.order_by(
            '-date'
        )

    elif sort == 'amount':
        expenses = expenses.order_by(
            '-amount'
        )

    elif sort == 'category':
        expenses = expenses.order_by(
            'category__name'
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

    cars = Car.objects.filter(
        owner=request.user
    )

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
            'sort': sort,
        }
    )

@login_required
def car_update(request, pk):

    car = get_object_or_404(
        Car,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':

        form = CarForm(
            request.POST,
            instance=car
        )

        if form.is_valid():
            form.save()

            return redirect(
                'car_list'
            )

    else:

        form = CarForm(
            instance=car
        )

    return render(
        request,
        'cars/car_form.html',
        {'form': form}
    )

@login_required
def car_delete(request, pk):

    car = get_object_or_404(
        Car,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':

        car.delete()

        return redirect(
            'car_list'
        )

    return render(
        request,
        'cars/car_confirm_delete.html',
        {'car': car}
    )

@login_required
def expense_update(request, pk):

    expense = get_object_or_404(
        Expense,
        pk=pk,
        car__owner=request.user
    )

    if request.method == 'POST':

        form = ExpenseForm(
            request.POST,
            instance=expense
        )

        if form.is_valid():
            form.save()

            return redirect(
                'expense_list'
            )

    else:

        form = ExpenseForm(
            instance=expense
        )

    form.fields['car'].queryset = (
        Car.objects.filter(
            owner=request.user
        )
    )

    return render(
        request,
        'cars/expense_form.html',
        {'form': form}
    )

@login_required
def expense_delete(request, pk):

    expense = get_object_or_404(
        Expense,
        pk=pk,
        car__owner=request.user
    )

    if request.method == 'POST':

        expense.delete()

        return redirect(
            'expense_list'
        )

    return render(
        request,
        'cars/expense_confirm_delete.html',
        {'expense': expense}
    )

@login_required
def analytics(request):

    expenses = Expense.objects.filter(
        car__owner=request.user
    )

    total_amount = (
        expenses.aggregate(
            total=Sum('amount')
        )['total']
        or 0
    )

    expense_count = expenses.count()

    average_expense = 0

    if expense_count:
        average_expense = (
            total_amount /
            expense_count
        )

    category_stats = (
        expenses
        .values('category__name')
        .annotate(
            total=Sum('amount')
        )
        .order_by('-total')
    )

    top_category = None

    if category_stats:
        top_category = category_stats[0]

    monthly_stats = (
        expenses
        .annotate(
            month=TruncMonth('date')
        )
        .values('month')
        .annotate(
            total=Sum('amount')
        )
        .order_by('month')
    )

    month_labels = []
    month_totals = []

    for item in monthly_stats:

        month_labels.append(
            item['month'].strftime('%m.%Y')
        )

        month_totals.append(
            float(item['total'])
        )

    return render(
        request,
        'cars/analytics.html',
        {
            'total_amount': total_amount,
            'expense_count': expense_count,
            'average_expense': average_expense,
            'top_category': top_category,
            'month_labels': json.dumps(month_labels),
            'month_totals': json.dumps(month_totals),
        }
    )