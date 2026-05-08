from django.db import models
from django.conf import settings
from trips.models import Trip
from PIL import Image
import io
from django.core.files.base import ContentFile

class Photo(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='photos')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='trip_photos/gallery/')
    caption = models.TextField(max_length=500, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            # Resize if too large
            if img.height > 1200 or img.width > 1200:
                output_size = (1200, 1200)
                img.thumbnail(output_size)
            
            # Compress
            img_io = io.BytesIO()
            # Convert to RGB if necessary (for PNGs with alpha)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(img_io, format='JPEG', quality=70)
            self.image.save(self.image.name, ContentFile(img_io.getvalue()), save=False)
            
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-uploaded_at']

class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

class Reaction(models.Model):
    REACTION_TYPES = [('like', 'Like'), ('love', 'Love'), ('amazing', 'Amazing')]
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='reactions', null=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='reactions', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20, choices=REACTION_TYPES)
    class Meta:
        unique_together = [('user', 'photo'), ('user', 'trip')]
