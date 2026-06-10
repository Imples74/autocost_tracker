from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    brand = models.CharField(
        max_length=100
    )

    model = models.CharField(
        max_length=100
    )

    year = models.PositiveIntegerField()

    fuel_type = models.CharField(
        max_length=50
    )

    engine_volume = models.FloatField()

    mileage = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.brand} {self.model}"

class ExpenseCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name

class Expense(models.Model):

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    date = models.DateField()

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.car} - "
            f"{self.category} - "
            f"{self.amount}"
        )