from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CarForm, ExpenseFilterForm, ExpenseForm
from .models import Car, Expense


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