from django.shortcuts import redirect, get_object_or_404
from .models import ItineraryItem
from trips.models import Trip
def itinerary_create(request, trip_pk):
    trip = get_object_or_404(Trip, pk=trip_pk, user=request.user)
    if request.method == 'POST':
        ItineraryItem.objects.create(trip=trip, date=request.POST.get('date'), time=request.POST.get('time') or None, activity=request.POST.get('activity'))
    return redirect('trip_detail', pk=trip_pk)
