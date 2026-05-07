from django.shortcuts import redirect, get_object_or_404
from .models import Expense
from trips.models import Trip
def expense_create(request, trip_pk):
    trip = get_object_or_404(Trip, pk=trip_pk, user=request.user)
    if request.method == 'POST':
        Expense.objects.create(trip=trip, date=request.POST.get('date'), category=request.POST.get('category'), amount=request.POST.get('amount'), description=request.POST.get('description'))
    return redirect('trip_detail', pk=trip_pk)
