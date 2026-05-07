from django.urls import path
from . import views
urlpatterns = [
    path('trips/<int:trip_pk>/photo/upload/', views.photo_upload, name='photo_upload'),
    path('photos/<int:pk>/', views.photo_detail, name='photo_detail'),
]
