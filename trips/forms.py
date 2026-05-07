from django import forms
from .models import Trip
class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'description', 'destination', 'start_date', 'end_date', 'trip_photo']
        widgets = {'start_date': forms.DateInput(attrs={'type': 'date'}), 'end_date': forms.DateInput(attrs={'type': 'date'})}
