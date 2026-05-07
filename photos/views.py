from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo, Comment, Reaction
from trips.models import Trip
def photo_upload(request, trip_pk):
    trip = get_object_or_404(Trip, pk=trip_pk, user=request.user)
    if request.method == 'POST': Photo.objects.create(trip=trip, user=request.user, image=request.FILES.get('image'), caption=request.POST.get('caption'))
    return redirect('trip_detail', pk=trip_pk)
def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photos/photo_detail.html', {'photo': photo})
