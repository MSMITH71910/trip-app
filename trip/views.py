# trip/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.db import connection
import os

from .models import Trip, ItineraryItem, BudgetItem, TripPhoto, Comment, PhotoComment, Reaction, UserProfile
from .forms import (
    SignUpForm, TripForm, TripPhotoUpdateForm, ItineraryItemForm,
    BudgetItemForm, TripPhotoForm, CommentForm, 
    PhotoCommentForm, UserProfileForm, UserSettingsForm, ReactionForm
)

def index(request):
    """Home page view showing recent trips."""
    # Get the most recent 6 trips to showcase on the homepage
    recent_trips = Trip.objects.all().order_by('-created_at')[:6]
    return render(request, 'trip/index.html', {
        'recent_trips': recent_trips
    })

def health_check(request):
    """Health check endpoint for debugging deployment issues."""
    try:
        # Basic Django check first
        django_status = "Django OK"
        
        # Test database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                db_status = "OK"
        except Exception as db_e:
            db_status = f"ERROR: {str(db_e)}"
        
        return JsonResponse({
            'status': 'OK',
            'django': django_status,
            'database': db_status,
            'environment': {
                'DEBUG': os.getenv('DJANGO_DEBUG', 'Not Set'),
                'DATABASE_URL': 'Set' if os.getenv('DATABASE_URL') else 'Not Set',
                'SECRET_KEY': 'Set' if os.getenv('DJANGO_SECRET_KEY') else 'Not Set',
                'VERCEL': 'Set' if os.getenv('VERCEL') else 'Not Set',
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'ERROR',
            'error': str(e),
            'environment': {
                'DEBUG': os.getenv('DJANGO_DEBUG', 'Not Set'),
                'DATABASE_URL': 'Set' if os.getenv('DATABASE_URL') else 'Not Set',
                'SECRET_KEY': 'Set' if os.getenv('DJANGO_SECRET_KEY') else 'Not Set',
                'VERCEL': 'Set' if os.getenv('VERCEL') else 'Not Set',
            }
        })

def simple_test(request):
    """Simple test endpoint that should always work."""
    return JsonResponse({
        'message': 'Django is working!',
        'timestamp': str(timezone.now()) if 'timezone' in globals() else 'No timezone',
        'environment_vars': {
            'SECRET_KEY': 'Set' if os.getenv('DJANGO_SECRET_KEY') else 'Not Set',
            'DEBUG': os.getenv('DJANGO_DEBUG', 'Not Set'),
            'DATABASE_URL': 'Set' if os.getenv('DATABASE_URL') else 'Not Set',
        }
    })

def terms_and_conditions(request):
    """Terms and Conditions page."""
    return render(request, 'trip/terms_and_conditions.html')

def signup(request):
    """User registration view."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f'Welcome to Trip Planner, {user.first_name}! Your account has been created successfully!')
            return redirect('trip:profile')
    else:
        form = SignUpForm()
    return render(request, 'trip/signup.html', {'form': form})

def login_view(request):
    """User login view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('trip:profile')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'trip/login.html')

def logout_view(request):
    """User logout view."""
    logout(request)
    return redirect('trip:index')

@login_required
def profile(request):
    """User profile view showing user's trips."""
    trips = Trip.objects.filter(user=request.user)
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Handle profile photo update
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile photo updated successfully!')
            return redirect('trip:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'trip/profile.html', {
        'trips': trips,
        'profile': profile,
        'form': form
    })

@login_required
def trip_new(request):
    """Create a new trip."""
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            messages.success(request, 'Trip created successfully!')
            return redirect('trip:trip_detail', trip_id=trip.id)
    else:
        form = TripForm()
    return render(request, 'trip/trip_form.html', {'form': form})

@login_required
def trip_detail(request, trip_id):
    """View trip details."""
    # Allow access to any trip, not just user's own trips
    trip = get_object_or_404(Trip, id=trip_id)
    itinerary_items = ItineraryItem.objects.filter(trip=trip)
    budget_items = BudgetItem.objects.filter(trip=trip)
    photos = TripPhoto.objects.filter(trip=trip)
    comments = Comment.objects.filter(trip=trip)
    
    # Determine if the current user is the owner of the trip
    is_owner = (trip.user == request.user)
    
    # Prefetch photo comments to improve performance
    photos = photos.prefetch_related('comments', 'comments__user')
    
    # Get the user's current reaction to this trip (if any)
    user_reaction = None
    user_reaction_obj = Reaction.objects.filter(user=request.user, trip=trip).first()
    if user_reaction_obj:
        user_reaction = user_reaction_obj.reaction_type
    
    # Get reaction counts by type for the trip
    reaction_counts = {}
    for reaction_type, _ in Trip.REACTION_CHOICES:
        reaction_counts[reaction_type] = Reaction.objects.filter(trip=trip, reaction_type=reaction_type).count()
    
    # Get reaction counts by type for each photo
    photo_reaction_counts = {}
    for photo in photos:
        photo_reaction_counts[photo.id] = {}
        for reaction_type, _ in Trip.REACTION_CHOICES:
            photo_reaction_counts[photo.id][reaction_type] = Reaction.objects.filter(
                photo=photo, reaction_type=reaction_type).count()
    
    # Calculate total budget
    total_budget = sum(item.amount for item in budget_items)
    
    context = {
        'trip': trip,
        'itinerary_items': itinerary_items,
        'budget_items': budget_items,
        'photos': photos,
        'comments': comments,
        'total_budget': total_budget,
        'user_reaction': user_reaction,
        'reaction_counts': reaction_counts,
        'photo_reaction_counts': photo_reaction_counts,
        'is_owner': is_owner,
    }
    return render(request, 'trip/trip_detail.html', context)

@login_required
def itinerary_add(request, trip_id):
    """Add an itinerary item to a trip."""
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    
    if request.method == 'POST':
        form = ItineraryItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.trip = trip
            item.save()
            messages.success(request, 'Itinerary item added successfully!')
            return redirect('trip:trip_detail', trip_id=trip.id)
    else:
        # Pre-fill the date with the trip start date
        form = ItineraryItemForm(initial={'date': trip.start_date})
    
    return render(request, 'trip/itinerary_form.html', {'form': form, 'trip': trip})

@login_required
def budget_add(request, trip_id):
    """Add a budget item to a trip."""
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    
    if request.method == 'POST':
        form = BudgetItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.trip = trip
            item.save()
            messages.success(request, 'Budget item added successfully!')
            return redirect('trip:trip_detail', trip_id=trip.id)
    else:
        form = BudgetItemForm()
    
    return render(request, 'trip/budget_form.html', {'form': form, 'trip': trip})

# Share trip functionality has been replaced with Download as PDF

@login_required
def print_trip(request, trip_id):
    """View for printing trip details."""
    trip = get_object_or_404(Trip, id=trip_id)
    itinerary_items = ItineraryItem.objects.filter(trip=trip)
    budget_items = BudgetItem.objects.filter(trip=trip)
    photos = TripPhoto.objects.filter(trip=trip)
    
    # Calculate total budget
    total_budget = sum(item.amount for item in budget_items)
    
    from datetime import datetime
    context = {
        'trip': trip,
        'itinerary_items': itinerary_items,
        'budget_items': budget_items,
        'photos': photos,
        'total_budget': total_budget,
        'now': datetime.now(),
    }
    return render(request, 'trip/print_trip.html', context)

@login_required
def add_photo(request, trip_id):
    """Add a photo to a trip."""
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    
    if request.method == 'POST':
        form = TripPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.trip = trip
            photo.save()
            messages.success(request, 'Photo added successfully!')
            return redirect('trip:trip_detail', trip_id=trip.id)
    else:
        form = TripPhotoForm()
    
    return render(request, 'trip/add_photo.html', {'form': form, 'trip': trip})

@login_required
def add_comment(request, trip_id):
    """Add a comment to a trip."""
    trip = get_object_or_404(Trip, id=trip_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.trip = trip
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('trip:trip_detail', trip_id=trip.id)
    else:
        form = CommentForm()
    
    return render(request, 'trip/add_comment.html', {'form': form, 'trip': trip})

@login_required
def react(request, trip_id, reaction_type):
    """Add or update a reaction to a trip."""
    trip = get_object_or_404(Trip, id=trip_id)
    
    # No longer checking if user is trip owner - anyone can react
    
    # Check if the user already has a reaction
    existing_reaction = Reaction.objects.filter(user=request.user, trip=trip).first()
    
    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            # If same reaction, remove it (toggle off)
            existing_reaction.delete()
            messages.success(request, 'Reaction removed.')
        else:
            # If different reaction, update it
            existing_reaction.reaction_type = reaction_type
            existing_reaction.save()
            messages.success(request, 'Reaction updated.')
    else:
        # Create new reaction
        reaction = Reaction(
            user=request.user,
            trip=trip,
            reaction_type=reaction_type
        )
        reaction.save()
        messages.success(request, 'Reaction added.')
    
    return redirect('trip:trip_detail', trip_id=trip.id)

@login_required
def explore(request):
    """View for exploring all trips."""
    trips = Trip.objects.all().order_by('-created_at')
    return render(request, 'trip/explore.html', {
        'trips': trips
    })

def react_photo(request, photo_id, reaction_type):
    """Add or update a reaction to a photo."""
    photo = get_object_or_404(TripPhoto, id=photo_id)
    trip = photo.trip
    
    # No longer checking if user is trip owner - anyone can react
    
    # Check if the user already has a reaction
    existing_reaction = Reaction.objects.filter(user=request.user, photo=photo).first()
    
    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            # If same reaction, remove it (toggle off)
            existing_reaction.delete()
            messages.success(request, 'Reaction removed.')
        else:
            # If different reaction, update it
            existing_reaction.reaction_type = reaction_type
            existing_reaction.save()
            messages.success(request, 'Reaction updated.')
    else:
        # Create new reaction
        reaction = Reaction(
            user=request.user,
            photo=photo,
            reaction_type=reaction_type
        )
        reaction.save()
        messages.success(request, 'Reaction added.')
    
    return redirect('trip:trip_detail', trip_id=trip.id)

@login_required
def add_photo_comment(request, photo_id):
    """Add a comment to a photo."""
    photo = get_object_or_404(TripPhoto, id=photo_id)
    trip = photo.trip
    
    # No longer checking if user is trip owner - anyone can comment
    
    if request.method == 'POST':
        form = PhotoCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = photo
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added to photo successfully!')
            return redirect('trip:trip_detail', trip_id=trip.id)
    else:
        form = PhotoCommentForm()
    
    return render(request, 'trip/add_photo_comment.html', {
        'form': form, 
        'photo': photo,
        'trip': trip
    })

@login_required
def react_comment(request, comment_id, reaction_type):
    """Add or update a reaction to a comment."""
    comment = get_object_or_404(Comment, id=comment_id)
    trip = comment.trip
    
    # No longer checking if user is trip owner - anyone can react
    
    # Check if the user already has a reaction
    existing_reaction = Reaction.objects.filter(user=request.user, comment=comment).first()
    
    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            # If same reaction, remove it (toggle off)
            existing_reaction.delete()
            messages.success(request, 'Reaction removed.')
        else:
            # If different reaction, update it
            existing_reaction.reaction_type = reaction_type
            existing_reaction.save()
            messages.success(request, 'Reaction updated.')
    else:
        # Create new reaction
        reaction = Reaction(
            user=request.user,
            comment=comment,
            reaction_type=reaction_type
        )
        reaction.save()
        messages.success(request, 'Reaction added.')
    
    return redirect('trip:trip_detail', trip_id=trip.id)

@login_required
def react_photo_comment(request, photo_comment_id, reaction_type):
    """Add or update a reaction to a photo comment."""
    photo_comment = get_object_or_404(PhotoComment, id=photo_comment_id)
    trip = photo_comment.photo.trip
    
    # No longer checking if user is trip owner - anyone can react
    
    # Check if the user already has a reaction
    existing_reaction = Reaction.objects.filter(user=request.user, photo_comment=photo_comment).first()
    
    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            # If same reaction, remove it (toggle off)
            existing_reaction.delete()
            messages.success(request, 'Reaction removed.')
        else:
            # If different reaction, update it
            existing_reaction.reaction_type = reaction_type
            existing_reaction.save()
            messages.success(request, 'Reaction updated.')
    else:
        # Create new reaction
        reaction = Reaction(
            user=request.user,
            photo_comment=photo_comment,
            reaction_type=reaction_type
        )
        reaction.save()
        messages.success(request, 'Reaction added.')
    
    return redirect('trip:trip_detail', trip_id=trip.id)

@login_required
def delete_trip(request, trip_id):
    """Delete a trip."""
    # Only allow the owner to delete their own trip
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    
    if request.method == 'POST':
        # Delete the trip and all related items
        trip.delete()
        messages.success(request, 'Trip deleted successfully!')
        return redirect('trip:profile')
    
    # Confirm deletion page
    return render(request, 'trip/delete_trip.html', {'trip': trip})

@login_required
def update_trip_photo(request, trip_id):
    """Update a trip's profile photo."""
    # Only allow the owner to update their own trip
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    
    if request.method == 'POST':
        form = TripPhotoUpdateForm(request.POST, request.FILES, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trip photo updated successfully!')
            return redirect('trip:trip_detail', trip_id=trip.id)
    else:
        form = TripPhotoUpdateForm(instance=trip)
    
    return render(request, 'trip/update_trip_photo.html', {'form': form, 'trip': trip})

@login_required
def delete_photo(request, photo_id):
    """Delete a photo from a trip."""
    photo = get_object_or_404(TripPhoto, id=photo_id)
    trip = photo.trip
    
    # Only allow the owner to delete photos from their own trip
    if trip.user != request.user:
        messages.error(request, 'You do not have permission to delete this photo.')
        return redirect('trip:trip_detail', trip_id=trip.id)
    
    if request.method == 'POST':
        photo.delete()
        messages.success(request, 'Photo deleted successfully!')
        return redirect('trip:trip_detail', trip_id=trip.id)
    
    return render(request, 'trip/delete_photo.html', {'photo': photo, 'trip': trip})

@login_required
def delete_comment(request, comment_id):
    """Delete a comment from a trip."""
    comment = get_object_or_404(Comment, id=comment_id)
    trip = comment.trip
    
    # Only allow the comment author or trip owner to delete the comment
    if comment.user != request.user and trip.user != request.user:
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('trip:trip_detail', trip_id=trip.id)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('trip:trip_detail', trip_id=trip.id)
    
    return render(request, 'trip/delete_comment.html', {'comment': comment, 'trip': trip})

@login_required
def delete_photo_comment(request, comment_id):
    """Delete a comment from a photo."""
    comment = get_object_or_404(PhotoComment, id=comment_id)
    photo = comment.photo
    trip = photo.trip
    
    # Only allow the comment author or trip owner to delete the comment
    if comment.user != request.user and trip.user != request.user:
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('trip:trip_detail', trip_id=trip.id)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('trip:trip_detail', trip_id=trip.id)
    
    return render(request, 'trip/delete_photo_comment.html', {'comment': comment, 'photo': photo, 'trip': trip})

@login_required
def edit_comment(request, comment_id):
    """Edit a comment on a trip."""
    comment = get_object_or_404(Comment, id=comment_id)
    trip = comment.trip
    
    # Only allow the comment author to edit the comment
    if comment.user != request.user:
        messages.error(request, 'You do not have permission to edit this comment.')
        return redirect('trip:trip_detail', trip_id=trip.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('trip:trip_detail', trip_id=trip.id)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'trip/edit_comment.html', {'form': form, 'comment': comment, 'trip': trip})

@login_required
def edit_photo_comment(request, comment_id):
    """Edit a comment on a photo."""
    comment = get_object_or_404(PhotoComment, id=comment_id)
    photo = comment.photo
    trip = photo.trip
    
    # Only allow the comment author to edit the comment
    if comment.user != request.user:
        messages.error(request, 'You do not have permission to edit this comment.')
        return redirect('trip:trip_detail', trip_id=trip.id)
    
    if request.method == 'POST':
        form = PhotoCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('trip:trip_detail', trip_id=trip.id)
    else:
        form = PhotoCommentForm(instance=comment)
    
    return render(request, 'trip/edit_photo_comment.html', {'form': form, 'comment': comment, 'photo': photo, 'trip': trip})

@login_required
def user_portfolio(request, username=None):
    """Display user portfolio page."""
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Check if the requesting user can view this profile
    if not profile.can_view_profile(request.user):
        messages.error(request, 'This profile is private.')
        return redirect('trip:index')
    
    # Get user's trips if they can be viewed
    trips = []
    if profile.can_view_trips(request.user):
        trips = Trip.objects.filter(user=user).order_by('-created_at')
    
    # Get featured trips
    featured_trips = profile.get_featured_trips()
    
    context = {
        'profile_user': user,
        'profile': profile,
        'trips': trips,
        'featured_trips': featured_trips,
        'trip_count': profile.get_trip_count() if profile.show_trip_count else None,
        'photo_count': profile.get_photo_count(),
        'is_own_profile': request.user == user,
    }
    
    return render(request, 'trip/user_portfolio.html', context)

@login_required
def edit_portfolio(request):
    """Edit user portfolio information."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Portfolio updated successfully!')
            return redirect('trip:user_portfolio')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'trip/edit_portfolio.html', {'form': form, 'profile': profile})

@login_required
def user_settings(request):
    """User settings page."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            # Clear existing featured trips and set new ones
            profile.featured_trips.clear()
            for trip in form.cleaned_data['featured_trips']:
                profile.featured_trips.add(trip)
            
            form.save()
            messages.success(request, 'Settings updated successfully!')
            return redirect('trip:user_settings')
    else:
        form = UserSettingsForm(instance=profile, user=request.user)
    
    return render(request, 'trip/user_settings.html', {'form': form, 'profile': profile})

def public_portfolio(request, username):
    """Public view of user portfolio."""
    return user_portfolio(request, username)