from django.db import models
from django.conf import settings
from django.utils import timezone

class Trip(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trips')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    destination = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    trip_photo = models.ImageField(upload_to='trip_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-start_date']
    def __str__(self):
        return self.title
    @property
    def is_past(self):
        return self.end_date < timezone.now().date()
    @property
    def is_future(self):
        return self.start_date > timezone.now().date()
    @property
    def duration(self):
        return (self.end_date - self.start_date).days + 1
