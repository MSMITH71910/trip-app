from django.urls import path
from . import views
urlpatterns = [path('trips/<int:trip_pk>/expense/add/', views.expense_create, name='expense_create')]
