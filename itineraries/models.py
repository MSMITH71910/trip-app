from django.db import models
from trips.models import Trip

class ItineraryItem(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='itinerary_items')
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    activity = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    class Meta:
        ordering = ['date', 'time']
    def __str__(self):
        return f"{self.date} {self.activity}"
