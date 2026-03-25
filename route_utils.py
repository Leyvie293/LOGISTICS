import requests
import os
from config import Config

ORS_API_KEY = Config.ORS_API_KEY

def geocode_address(address):
    """
    Convert address string to (lat, lng) using OpenRouteService geocoding.
    Returns tuple (latitude, longitude) or None if failed.
    """
    url = "https://api.openrouteservice.org/geocode/search"
    params = {
        'api_key': ORS_API_KEY,
        'text': address,
        'size': 1
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data['features']:
            coords = data['features'][0]['geometry']['coordinates']
            return coords[1], coords[0]  # (lat, lng)
    except:
        pass
    return None, None

def get_distance_and_time(start_addr, end_addr):
    """
    Get distance (km) and duration (seconds) between two addresses.
    Returns tuple (distance_km, duration_sec) or (None, None) on failure.
    """
    # Geocode addresses
    start_lat, start_lng = geocode_address(start_addr)
    end_lat, end_lng = geocode_address(end_addr)
    if None in (start_lat, end_lat):
        return None, None

    # Use OpenRouteService directions
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    params = {
        'api_key': ORS_API_KEY,
        'start': f"{start_lng},{start_lat}",
        'end': f"{end_lng},{end_lat}"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        distance = data['features'][0]['properties']['segments'][0]['distance'] / 1000  # km
        duration = data['features'][0]['properties']['segments'][0]['duration']  # seconds
        return distance, duration
    except:
        return None, None