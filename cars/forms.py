from django import forms
from .models import Car


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