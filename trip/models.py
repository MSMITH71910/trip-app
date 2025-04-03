# trip/models.py

from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):
    REACTION_CHOICES = [
        ('LIKE', 'Like'),
        ('LOVE', 'Love'),
        ('AMAZING', 'Amazing'),
        ('INTERESTING', 'Interesting'),
        ('DISLIKE', 'Dislike'),
        ('BORING', 'Boring'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_trips', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_trips', blank=True)
    profile_photo = models.ImageField(upload_to='trip_profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.title
        
    def get_profile_photo_url(self):
        if self.profile_photo:
            return self.profile_photo.url
        # Return a default image URL if no profile photo is set
        return '/static/trip/images/default-trip.svg'

    def get_reactions_count(self):
        return self.reactions.count()
        
    def get_reactions_by_type(self):
        reaction_counts = {}
        for choice in self.REACTION_CHOICES:
            reaction_counts[choice[0]] = self.reactions.filter(reaction_type=choice[0]).count()
        return reaction_counts

    class Meta:
        ordering = ['-start_date']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True)

class TripPhoto(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='trip_photos/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Comment by {self.user.username} on {self.trip.title}"
        
class PhotoComment(models.Model):
    photo = models.ForeignKey(TripPhoto, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Comment by {self.user.username} on photo in {self.photo.trip.title}"

class ItineraryItem(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    activity = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.activity} at {self.location}"

class BudgetItem(models.Model):
    CATEGORY_CHOICES = [
        ('TRANSPORT', 'Transportation'),
        ('ACCOMMODATION', 'Accommodation'),
        ('FOOD', 'Food & Drinks'),
        ('ACTIVITIES', 'Activities'),
        ('OTHER', 'Other'),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.get_category_display()}: {self.description}"
        
class Reaction(models.Model):
    REACTION_CHOICES = [
        ('LIKE', 'Like'),
        ('LOVE', 'Love'),
        ('AMAZING', 'Amazing'),
        ('INTERESTING', 'Interesting'),
        ('DISLIKE', 'Dislike'),
        ('BORING', 'Boring'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Optional foreign keys for different content types
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True, blank=True, related_name='reactions')
    photo = models.ForeignKey(TripPhoto, on_delete=models.CASCADE, null=True, blank=True, related_name='reactions')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name='reactions')
    photo_comment = models.ForeignKey(PhotoComment, on_delete=models.CASCADE, null=True, blank=True, related_name='reactions')
    
    class Meta:
        unique_together = [
            ('user', 'trip'),
            ('user', 'photo'),
            ('user', 'comment'),
            ('user', 'photo_comment'),
        ]
        
    def __str__(self):
        if self.trip:
            return f"{self.user.username} - {self.get_reaction_type_display()} - Trip: {self.trip.title}"
        elif self.photo:
            return f"{self.user.username} - {self.get_reaction_type_display()} - Photo: {self.photo.caption or 'Untitled'}"
        elif self.comment:
            return f"{self.user.username} - {self.get_reaction_type_display()} - Comment"
        elif self.photo_comment:
            return f"{self.user.username} - {self.get_reaction_type_display()} - Photo Comment"
        return f"{self.user.username} - {self.get_reaction_type_display()}"