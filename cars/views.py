import json
from datetime import date
from decimal import Decimal

import pandas as pd
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CarForm, ExpenseFilterForm, ExpenseForm, RegisterForm
from .models import Car, Expense, MonthlyForecast


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('car_list')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {
        'form': form,
    })


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


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(
        car__user=request.user
    ).select_related('car', 'category')

    filter_form = ExpenseFilterForm(
        request.GET or None,
        user=request.user
    )

    if filter_form.is_valid():
        car = filter_form.cleaned_data.get('car')
        category = filter_form.cleaned_data.get('category')
        date_from = filter_form.cleaned_data.get('date_from')
        date_to = filter_form.cleaned_data.get('date_to')

        if car:
            expenses = expenses.filter(car=car)

        if category:
            expenses = expenses.filter(category=category)

        if date_from:
            expenses = expenses.filter(expense_date__gte=date_from)

        if date_to:
            expenses = expenses.filter(expense_date__lte=date_to)

    return render(request, 'cars/expense_list.html', {
        'expenses': expenses,
        'filter_form': filter_form,
    })


@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)

        if form.is_valid():
            expense = form.save(commit=False)

            if expense.car.user != request.user:
                return redirect('expense_list')

            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(user=request.user)

    return render(request, 'cars/expense_form.html', {
        'form': form,
        'title': 'Добавить расход',
        'button_text': 'Добавить',
    })


@login_required
def expense_create_for_car(request, car_pk):
    car = get_object_or_404(
        Car,
        pk=car_pk,
        user=request.user
    )

    if request.method == 'POST':
        form = ExpenseForm(
            request.POST,
            user=request.user,
            selected_car=car
        )

        if form.is_valid():
            expense = form.save(commit=False)
            expense.car = car
            expense.save()
            return redirect('car_detail', pk=car.pk)
    else:
        form = ExpenseForm(
            user=request.user,
            selected_car=car
        )

    return render(request, 'cars/expense_form.html', {
        'form': form,
        'title': f'Добавить расход для {car.brand} {car.model}',
        'button_text': 'Добавить',
    })


@login_required
def expense_update(request, pk):
    expense = get_object_or_404(
        Expense,
        pk=pk,
        car__user=request.user
    )

    if request.method == 'POST':
        form = ExpenseForm(
            request.POST,
            instance=expense,
            user=request.user
        )

        if form.is_valid():
            updated_expense = form.save(commit=False)

            if updated_expense.car.user != request.user:
                return redirect('expense_list')

            updated_expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(
            instance=expense,
            user=request.user
        )

    return render(request, 'cars/expense_form.html', {
        'form': form,
        'title': 'Редактировать расход',
        'button_text': 'Сохранить',
    })


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(
        Expense,
        pk=pk,
        car__user=request.user
    )

    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')

    return render(request, 'cars/expense_confirm_delete.html', {
        'expense': expense,
    })


def get_next_month_first_day():
    today = date.today()

    if today.month == 12:
        return date(today.year + 1, 1, 1)

    return date(today.year, today.month + 1, 1)


@login_required
def analytics(request):
    cars = Car.objects.filter(user=request.user)

    selected_car = None
    selected_car_id = request.GET.get('car')

    if selected_car_id:
        selected_car = cars.filter(pk=selected_car_id).first()

    if selected_car is None:
        selected_car = cars.first()

    context = {
        'cars': cars,
        'selected_car': selected_car,
        'has_expenses': False,
        'total_amount': 0,
        'average_monthly_amount': 0,
        'top_category': None,
        'forecast_amount': None,
        'forecast_month': None,
        'month_labels_json': json.dumps([]),
        'month_values_json': json.dumps([]),
        'category_labels_json': json.dumps([]),
        'category_values_json': json.dumps([]),
    }

    if selected_car is None:
        return render(request, 'cars/analytics.html', context)

    expenses = Expense.objects.filter(
        car=selected_car,
        car__user=request.user
    ).select_related('category')

    if not expenses.exists():
        return render(request, 'cars/analytics.html', context)

    expense_data = []

    for expense in expenses:
        expense_data.append({
            'expense_date': expense.expense_date,
            'category': expense.category.name,
            'amount': float(expense.amount),
        })

    df = pd.DataFrame(expense_data)

    df['month'] = pd.to_datetime(df['expense_date']).dt.to_period('M').astype(str)

    total_amount = round(df['amount'].sum(), 2)

    monthly_data = (
        df.groupby('month')['amount']
        .sum()
        .reset_index()
        .sort_values('month')
    )

    category_data = (
        df.groupby('category')['amount']
        .sum()
        .reset_index()
        .sort_values('amount', ascending=False)
    )

    average_monthly_amount = round(monthly_data['amount'].mean(), 2)

    top_category_row = category_data.iloc[0]
    top_category = {
        'name': top_category_row['category'],
        'amount': round(top_category_row['amount'], 2),
    }

    last_three_months = monthly_data.tail(3)
    forecast_amount = round(last_three_months['amount'].mean(), 2)
    forecast_month = get_next_month_first_day()

    MonthlyForecast.objects.update_or_create(
        car=selected_car,
        forecast_month=forecast_month,
        defaults={
            'predicted_amount': Decimal(str(forecast_amount)),
            'calculation_description': (
                'Прогноз рассчитан как среднее значение расходов '
                'за последние доступные месяцы, максимум за 3 месяца.'
            ),
        }
    )

    context.update({
        'has_expenses': True,
        'total_amount': total_amount,
        'average_monthly_amount': average_monthly_amount,
        'top_category': top_category,
        'forecast_amount': forecast_amount,
        'forecast_month': forecast_month,
        'month_labels_json': json.dumps(monthly_data['month'].tolist()),
        'month_values_json': json.dumps(monthly_data['amount'].round(2).tolist()),
        'category_labels_json': json.dumps(category_data['category'].tolist()),
        'category_values_json': json.dumps(category_data['amount'].round(2).tolist()),
    })

    return render(request, 'cars/analytics.html', context)