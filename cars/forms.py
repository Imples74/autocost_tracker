from datetime import date

from django import forms

from .models import Car, Expense, ExpenseCategory


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


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'car',
            'category',
            'amount',
            'expense_date',
            'mileage',
            'description',
        ]
        labels = {
            'car': 'Автомобиль',
            'category': 'Категория',
            'amount': 'Сумма',
            'expense_date': 'Дата расхода',
            'mileage': 'Пробег',
            'description': 'Описание',
        }
        widgets = {
            'expense_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        selected_car = kwargs.pop('selected_car', None)

        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['car'].queryset = Car.objects.filter(user=user)

        if selected_car is not None:
            self.fields['car'].initial = selected_car
            self.fields['car'].queryset = Car.objects.filter(pk=selected_car.pk)

        self.fields['category'].queryset = ExpenseCategory.objects.all()

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['car'].widget.attrs.update({
            'class': 'form-select'
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-select'
        })

    def clean_amount(self):
        amount = self.cleaned_data['amount']

        if amount <= 0:
            raise forms.ValidationError(
                'Сумма расхода должна быть больше нуля.'
            )

        return amount

    def clean_mileage(self):
        mileage = self.cleaned_data.get('mileage')

        if mileage is not None and mileage < 0:
            raise forms.ValidationError(
                'Пробег не может быть отрицательным.'
            )

        return mileage


class ExpenseFilterForm(forms.Form):
    car = forms.ModelChoiceField(
        queryset=Car.objects.none(),
        required=False,
        label='Автомобиль'
    )
    category = forms.ModelChoiceField(
        queryset=ExpenseCategory.objects.all(),
        required=False,
        label='Категория'
    )
    date_from = forms.DateField(
        required=False,
        label='Дата от',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        label='Дата до',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['car'].queryset = Car.objects.filter(user=user)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['car'].widget.attrs.update({
            'class': 'form-select'
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-select'
        })