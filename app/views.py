import math
from django.shortcuts import render
# import googlemaps # type: ignore
from django.shortcuts import render
from django.conf import settings
# import requests # type: ignore
# from geopy.distance import geodesic # type: ignore
from .models import Booking

import requests
from django.http import JsonResponse

def homepage(request):
    return render(request,'home.html')
 
def round(request):
    return render(request,'round.html')


# Haversine formula for calculating distance between two lat/long points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c  # Distance in km

def calculate_distance(request):
    pickup = request.GET.get('pickup')  # Pickup location
    drop = request.GET.get('drop')  # Drop location

    if pickup and drop:
        # Geocode pickup location
        pickup_url = f'https://nominatim.openstreetmap.org/search?format=json&q={pickup}&addressdetails=1&limit=1'
        drop_url = f'https://nominatim.openstreetmap.org/search?format=json&q={drop}&addressdetails=1&limit=1'

        pickup_response = requests.get(pickup_url)
        drop_response = requests.get(drop_url)

        if pickup_response.status_code == 200 and drop_response.status_code == 200:
            pickup_data = pickup_response.json()
            drop_data = drop_response.json()

            if pickup_data and drop_data:
                # Extract lat/lon from response
                pickup_lat = float(pickup_data[0].get('lat'))
                pickup_lon = float(pickup_data[0].get('lon'))
                drop_lat = float(drop_data[0].get('lat'))
                drop_lon = float(drop_data[0].get('lon'))

                # Calculate distance using Haversine formula
                distance = haversine(pickup_lat, pickup_lon, drop_lat, drop_lon)
                return JsonResponse({'distance': round(distance, 2)})
    
    return JsonResponse({'error': 'Unable to calculate distance'})

def get_location_suggestions(request):
    query = request.GET.get('q', '')  # Get query from the request
    if query:
        # Nominatim API endpoint
        url = f'https://nominatim.openstreetmap.org/search?format=json&q={query}&addressdetails=1&limit=5'
        
        # Make request to Nominatim API
        response = requests.get(url)
        
        # Check if the response is successful
        if response.status_code == 200:
            results = response.json()
            # Process results (you can change the fields based on your needs)
            suggestions = []
            for result in results:
                suggestion = {
                    'name': result.get('display_name'),
                    'lat': result.get('lat'),
                    'lon': result.get('lon')
                }
                suggestions.append(suggestion)
            return JsonResponse({'suggestions': suggestions})
    
    return JsonResponse({'suggestions': []})