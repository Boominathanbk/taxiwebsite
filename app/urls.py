from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('round',views.round, name='round'),
    path('calculate_distance',views.calculate_distance, name='calculate_distance'),
]