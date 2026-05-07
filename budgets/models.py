from django.db import models
from trips.models import Trip

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('transportation', 'Transportation'), ('accommodation', 'Accommodation'),
        ('food', 'Food'), ('activities', 'Activities'),
        ('shopping', 'Shopping'), ('other', 'Other'),
    ]
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    class Meta:
        ordering = ['-date']
    def __str__(self):
        return f"{self.category}: {self.amount}"
