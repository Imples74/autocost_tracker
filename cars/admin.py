from django.contrib import admin

from .models import Car, Expense, ExpenseCategory, MonthlyForecast


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'brand',
        'model',
        'year',
        'fuel_type',
        'mileage',
        'user',
        'created_at',
    )
    search_fields = (
        'brand',
        'model',
        'user__username',
    )
    list_filter = (
        'fuel_type',
        'year',
        'created_at',
    )


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_regular',
    )
    search_fields = (
        'name',
        'description',
    )
    list_filter = (
        'is_regular',
    )


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'car',
        'category',
        'amount',
        'expense_date',
        'mileage',
        'created_at',
    )
    search_fields = (
        'car__brand',
        'car__model',
        'category__name',
        'description',
    )
    list_filter = (
        'category',
        'expense_date',
        'created_at',
    )


@admin.register(MonthlyForecast)
class MonthlyForecastAdmin(admin.ModelAdmin):
    list_display = (
        'car',
        'forecast_month',
        'predicted_amount',
        'created_at',
    )
    search_fields = (
        'car__brand',
        'car__model',
        'calculation_description',
    )
    list_filter = (
        'forecast_month',
        'created_at',
    )