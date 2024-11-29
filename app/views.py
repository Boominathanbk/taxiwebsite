from django.shortcuts import render
import googlemaps
from django.shortcuts import render
from django.conf import settings
import requests
from geopy.distance import geodesic
from .models import Booking


def homepage(request):
    return render(request,'home.html')
 

# def calculate_distance(request):
#     if request.method == "POST":
#         lat1 = request.POST.get("lat1")        
#         lon1 = request.POST.get("lon1")         
#         lat2 = request.POST.get("lat2")       
#         lon2 = request.POST.get("lon2")
#         distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers
#         return render(request,'home.html')

def calculate_distance(request):
    distance = None
    error_message = None

    if request.method == "POST":
        pickup = request.POST.get('pickup')
        drop = request.POST.get('drop')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        date = request.POST.get('date')

        if not all([pickup, drop, name, phone, email, date]):
            error_message = "All fields are required."
            return render(request, 'home.html', {'distance': distance, 'error_message': error_message})

        api_key = settings.GOOGLE_API_KEY

        def get_coordinates(location):
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                if data.get('status') == 'OK':
                    return data['results'][0]['geometry']['location'], None
                return None, data.get('error_message', 'Invalid location')
            except requests.exceptions.RequestException as e:
                return None, f"Error connecting to API: {e}"

        pickup_coords, pickup_error = get_coordinates(pickup)
        drop_coords, drop_error = get_coordinates(drop)

        if not pickup_coords:
            error_message = f"Pickup location error: {pickup_error}"
        elif not drop_coords:
            error_message = f"Drop location error: {drop_error}"
        else:
            try:
                distance = geodesic(
                    (pickup_coords['lat'], pickup_coords['lng']),
                    (drop_coords['lat'], drop_coords['lng'])
                ).kilometers

                Booking.objects.create(
                    pickup=pickup,
                    drop=drop,
                    name=name,
                    phone=phone,
                    email=email,
                    date=date,
                    distance=round(distance, 2)
                )
                print("datas save")
            except Exception as e:
                error_message = f"Error calculating or saving data: {e}"

    return render(request, 'home.html', {'distance': distance, 'error_message': error_message})



def round(request):
    return render(request,'round.html')