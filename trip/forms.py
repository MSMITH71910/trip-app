# trip/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Trip, ItineraryItem, BudgetItem, TripPhoto, Comment, PhotoComment, UserProfile, Reaction

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, 
        required=True,
        help_text='We\'ll never share your email with anyone else.'
    )
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        help_text='Your first name'
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        help_text='Your last name'
    )
    terms_accepted = forms.BooleanField(
        required=True,
        label='I agree to the Terms and Conditions',
        help_text='You must accept the terms and conditions to create an account.'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap styling
        for field_name in self.fields:
            if field_name == 'terms_accepted':
                self.fields[field_name].widget.attrs.update({'class': 'form-check-input'})
            else:
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})
        
        # Customize help text for password fields
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters and cannot be entirely numeric.'
        self.fields['password2'].help_text = 'Enter the same password as before, for verification.'

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'description', 'start_date', 'end_date', 'profile_photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
class TripPhotoUpdateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['profile_photo']
        widgets = {
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ItineraryItemForm(forms.ModelForm):
    class Meta:
        model = ItineraryItem
        fields = ['date', 'time', 'activity', 'location']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'activity': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BudgetItemForm(forms.ModelForm):
    class Meta:
        model = BudgetItem
        fields = ['category', 'description', 'amount']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

# ShareTripForm has been removed as we replaced Share Trip with Download as PDF

class TripPhotoForm(forms.ModelForm):
    class Meta:
        model = TripPhoto
        fields = ['photo', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }
        
class PhotoCommentForm(forms.ModelForm):
    class Meta:
        model = PhotoComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_photo']
        widgets = {
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'})
        }
        
class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['reaction_type']
        widgets = {
            'reaction_type': forms.Select(attrs={'class': 'form-control'})
        }