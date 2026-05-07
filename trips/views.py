from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Trip
from .forms import TripForm
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse

def home(request):
    if request.user.is_authenticated: return redirect('dashboard')
    return render(request, 'trips/home.html')
def explore(request):
    trips = Trip.objects.filter(user__trips_privacy='public')
    return render(request, 'trips/explore.html', {'trips': trips})
@login_required
def trip_create(request):
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save(commit=False); trip.user = request.user; trip.save()
            return redirect('trip_detail', pk=trip.pk)
    else: form = TripForm()
    return render(request, 'trips/trip_form.html', {'form': form})
@login_required
def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    total_cost = trip.expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'trips/trip_detail.html', {'trip': trip, 'total_cost': total_cost})
@login_required
def trip_pdf(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    template = get_template('trips/trip_pdf.html')
    html = template.render({'trip': trip, 'itinerary': trip.itinerary_items.all(), 'expenses': trip.expenses.all()})
    response = HttpResponse(content_type='application/pdf')
    pisa.CreatePDF(html, dest=response)
    return response
