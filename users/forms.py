from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
class CustomUserCreationForm(UserCreationForm):
    accepted_terms = forms.BooleanField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'accepted_terms')
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_photo', 'bio', 'location', 'theme_preference', 'profile_privacy', 'trips_privacy', 'photos_privacy']
