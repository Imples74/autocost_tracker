from django.contrib import admin
from .models import Car
from .models import (
    Car,
    ExpenseCategory,
    Expense
)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'brand',
        'model',
        'year',
        'fuel_type',
        'mileage',
    )

    search_fields = (
        'brand',
        'model',
    )

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):

    list_display = (
        'car',
        'category',
        'amount',
        'date'
    )

    list_filter = (
        'category',
        'date'
    )