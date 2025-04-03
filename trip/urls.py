# trip/urls.py

from django.urls import path
from . import views

app_name = 'trip'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('explore/', views.explore, name='explore'),
    path('trip/new/', views.trip_new, name='trip_new'),
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('trip/<int:trip_id>/delete/', views.delete_trip, name='delete_trip'),
    path('trip/<int:trip_id>/update-photo/', views.update_trip_photo, name='update_trip_photo'),
    path('trip/<int:trip_id>/itinerary/add/', views.itinerary_add, name='itinerary_add'),
    path('trip/<int:trip_id>/budget/add/', views.budget_add, name='budget_add'),

    path('trip/<int:trip_id>/print/', views.print_trip, name='print_trip'),
    path('trip/<int:trip_id>/add_photo/', views.add_photo, name='add_photo'),
    path('trip/<int:trip_id>/add_comment/', views.add_comment, name='add_comment'),
    path('trip/<int:trip_id>/react/<str:reaction_type>/', views.react, name='react'),
    path('photo/<int:photo_id>/react/<str:reaction_type>/', views.react_photo, name='react_photo'),
    path('photo/<int:photo_id>/add_comment/', views.add_photo_comment, name='add_photo_comment'),
    path('photo/<int:photo_id>/delete/', views.delete_photo, name='delete_photo'),
    path('comment/<int:comment_id>/react/<str:reaction_type>/', views.react_comment, name='react_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('photo_comment/<int:comment_id>/edit/', views.edit_photo_comment, name='edit_photo_comment'),
    path('photo_comment/<int:comment_id>/delete/', views.delete_photo_comment, name='delete_photo_comment'),
    path('photo_comment/<int:photo_comment_id>/react/<str:reaction_type>/', views.react_photo_comment, name='react_photo_comment'),
]