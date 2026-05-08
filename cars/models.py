from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Car(models.Model):
    FUEL_CHOICES = [
        ('petrol', 'Бензин'),
        ('diesel', 'Дизель'),
        ('gas', 'Газ'),
        ('hybrid', 'Гибрид'),
        ('electric', 'Электро'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cars',
        verbose_name='Пользователь'
    )
    brand = models.CharField(
        max_length=100,
        verbose_name='Марка'
    )
    model = models.CharField(
        max_length=100,
        verbose_name='Модель'
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска'
    )
    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_CHOICES,
        verbose_name='Тип топлива'
    )
    engine_volume = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name='Объем двигателя'
    )
    mileage = models.PositiveIntegerField(
        default=0,
        verbose_name='Пробег'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['brand', 'model']

    def __str__(self):
        return f'{self.brand} {self.model} ({self.year})'


class ExpenseCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название категории'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    is_regular = models.BooleanField(
        default=False,
        verbose_name='Регулярный расход'
    )

    class Meta:
        verbose_name = 'Категория расхода'
        verbose_name_plural = 'Категории расходов'
        ordering = ['name']

    def __str__(self):
        return self.name


class Expense(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='expenses',
        verbose_name='Автомобиль'
    )
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.PROTECT,
        related_name='expenses',
        verbose_name='Категория'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма'
    )
    expense_date = models.DateField(
        default=timezone.now,
        verbose_name='Дата расхода'
    )
    mileage = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Пробег на момент расхода'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'
        ordering = ['-expense_date', '-created_at']

    def __str__(self):
        return f'{self.car} — {self.category} — {self.amount} ₽'


class MonthlyForecast(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='forecasts',
        verbose_name='Автомобиль'
    )
    forecast_month = models.DateField(
        verbose_name='Месяц прогноза'
    )
    predicted_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Прогнозируемая сумма'
    )
    calculation_description = models.TextField(
        verbose_name='Описание расчета'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания прогноза'
    )

    class Meta:
        verbose_name = 'Прогноз расходов'
        verbose_name_plural = 'Прогнозы расходов'
        ordering = ['-forecast_month']

    def __str__(self):
        return f'{self.car} — прогноз на {self.forecast_month}'
