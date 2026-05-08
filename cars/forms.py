from datetime import date

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
        labels = {
            'brand': 'Марка',
            'model': 'Модель',
            'year': 'Год выпуска',
            'fuel_type': 'Тип топлива',
            'engine_volume': 'Объем двигателя',
            'mileage': 'Пробег',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['fuel_type'].widget.attrs.update({
            'class': 'form-select'
        })

    def clean_year(self):
        year = self.cleaned_data['year']
        current_year = date.today().year

        if year > current_year:
            raise forms.ValidationError(
                'Год выпуска не может быть больше текущего года.'
            )

        if year < 1950:
            raise forms.ValidationError(
                'Введите корректный год выпуска автомобиля.'
            )

        return year

    def clean_engine_volume(self):
        engine_volume = self.cleaned_data['engine_volume']

        if engine_volume <= 0:
            raise forms.ValidationError(
                'Объем двигателя должен быть больше нуля.'
            )

        return engine_volume