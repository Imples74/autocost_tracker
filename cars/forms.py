from django import forms
from .models import Car
from .models import Expense

class CarForm(forms.ModelForm):
    class Meta:
        model = Car

        fields = [
            'brand',
            'model',
            'year',
            'fuel_type',
            'engine_volume',
            'mileage',
        ]

class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense

        fields = [
            'car',
            'category',
            'amount',
            'date',
            'description',
        ]