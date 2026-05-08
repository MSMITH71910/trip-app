from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    THEME_CHOICES = [('light', 'Light'), ('dark', 'Dark'), ('auto', 'Auto')]
    PRIVACY_CHOICES = [('public', 'Public'), ('registered', 'Registered Users'), ('private', 'Private')]
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    instagram_url = models.URLField(max_length=200, blank=True)
    twitter_url = models.URLField(max_length=200, blank=True)
    facebook_url = models.URLField(max_length=200, blank=True)
    theme_preference = models.CharField(max_length=10, choices=THEME_CHOICES, default='auto')
    profile_privacy = models.CharField(max_length=15, choices=PRIVACY_CHOICES, default='public')
    trips_privacy = models.CharField(max_length=15, choices=PRIVACY_CHOICES, default='public')
    photos_privacy = models.CharField(max_length=15, choices=PRIVACY_CHOICES, default='public')
    notify_comments = models.BooleanField(default=True)
    notify_reactions = models.BooleanField(default=True)
    accepted_terms = models.BooleanField(default=False)

class FeaturedTrip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='featured_trips')
    trip = models.ForeignKey('trips.Trip', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)
    class Meta:
        ordering = ['order']
        unique_together = ('user', 'trip')
