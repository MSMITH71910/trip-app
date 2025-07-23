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

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'profile_photo', 'bio', 'location', 'website',
            'social_instagram', 'social_twitter', 'social_facebook'
        ]
        widgets = {
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Tell others about yourself and your travel experiences...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., New York, USA'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://yourwebsite.com'
            }),
            'social_instagram': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'your_username'
            }),
            'social_twitter': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'your_username'
            }),
            'social_facebook': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://facebook.com/yourprofile'
            }),
        }
        
        labels = {
            'social_twitter': 'X (Twitter)',
            'social_instagram': 'Instagram',
            'social_facebook': 'Facebook',
        }

class UserSettingsForm(forms.ModelForm):
    featured_trips = forms.ModelMultipleChoiceField(
        queryset=Trip.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='Select up to 3 trips to feature on your portfolio'
    )
    
    class Meta:
        model = UserProfile
        fields = [
            'profile_visibility', 'trips_visibility', 'photos_visibility', 'email_visibility',
            'theme_preference', 'show_trip_count', 'show_join_date', 'show_last_active',
            'email_notifications', 'comment_notifications', 'reaction_notifications',
            'featured_trips'
        ]
        widgets = {
            'profile_visibility': forms.Select(attrs={'class': 'form-select'}),
            'trips_visibility': forms.Select(attrs={'class': 'form-select'}),
            'photos_visibility': forms.Select(attrs={'class': 'form-select'}),
            'email_visibility': forms.Select(attrs={'class': 'form-select'}),
            'theme_preference': forms.Select(attrs={'class': 'form-select'}),
            'show_trip_count': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_join_date': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_last_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'comment_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'reaction_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['featured_trips'].queryset = Trip.objects.filter(user=user)
    
    def clean_featured_trips(self):
        featured_trips = self.cleaned_data.get('featured_trips')
        if featured_trips and len(featured_trips) > 3:
            raise forms.ValidationError('You can only select up to 3 featured trips.')
        return featured_trips

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

class UserProfilePhotoForm(forms.ModelForm):
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