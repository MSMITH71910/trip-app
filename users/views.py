from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm
from .models import User
from trips.models import Trip
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else: form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
@login_required
def dashboard(request):
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'users/dashboard.html', {'trips': trips})
@login_required
def settings_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings updated.")
            return redirect('settings')
    else: form = UserUpdateForm(instance=request.user)
    return render(request, 'users/settings.html', {'form': form})
def portfolio(request, username):
    profile_user = get_object_or_404(User, username=username)
    trips = Trip.objects.filter(user=profile_user)
    return render(request, 'users/portfolio.html', {'profile_user': profile_user, 'trips': trips})
