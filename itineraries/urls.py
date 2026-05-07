from django.urls import path
from . import views
urlpatterns = [path('trips/<int:trip_pk>/itinerary/add/', views.itinerary_create, name='itinerary_create')]
