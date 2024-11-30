from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('round',views.round, name='round'),
    path('location-suggestions/', views.get_location_suggestions, name='location_suggestions'),
    path('calculate-distance/', views.calculate_distance, name='calculate_distance'),
]