import ee
from django.shortcuts import render
from django.http import JsonResponse
from apps.gee.boundary_utils import get_country_centroid
from apps.gee.ndvi import get_ndvi
from apps.gee.soil_moisture import get_soil_moisture
from apps.gee.temperature import get_temperature
from apps.gee.rainfall import get_rainfall 


def _get_tile_url(image, vis_params):
    """Helper: get tile URL from an EE image."""
    map_id = image.getMapId(vis_params)
    return map_id["tile_fetcher"].url_format

# ========== NDVI VIEW ==========
def ndvi_map(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        try:
            image = get_ndvi(start_date, end_date)
            vis_params = {"min": 0, "max": 1, "palette": ["brown", "yellow", "green"]}
            tile_url = _get_tile_url(image, vis_params)
            return JsonResponse({"tile_url": tile_url})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # HTML render
    context = {
        'indicator_name': 'NDVI (Normalized Difference Vegetation Index)',
        'description': 'MODIS 16-day composite, 1km resolution. Average over selected date range.',
        'center_lat': get_country_centroid()['lat'],
        'center_lng': get_country_centroid()['lng'],
        'default_start': "2024-02-01",
        'default_end': "2024-02-16",
    }
    return render(request, 'indicators/indicator_map.html', context)

# ========== SOIL MOISTURE VIEW ==========
def soil_moisture_map(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        try:
            image = get_soil_moisture(start_date, end_date)
            vis_params = {"min": 0, "max": 0.5, "palette": ["brown", "orange", "lightblue", "blue"]}
            tile_url = _get_tile_url(image, vis_params)
            return JsonResponse({"tile_url": tile_url})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    context = {
        'indicator_name': 'Soil Moisture (Volumetric Water)',
        'description': 'ERA5-Land daily average, 0–0.5 m³/m³. Average over selected date range.',
        'center_lat': get_country_centroid()['lat'],
        'center_lng': get_country_centroid()['lng'],
        'default_start': "2024-02-01",
        'default_end': "2024-02-02",
    }
    return render(request, 'indicators/indicator_map.html', context)

# ========== TEMPERATURE VIEW ==========
def temperature_map(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        try:
            image = get_temperature(start_date, end_date)
            vis_params = {"min": 290, "max": 310, "palette": ["blue", "yellow", "red"]}
            tile_url = _get_tile_url(image, vis_params)
            return JsonResponse({"tile_url": tile_url})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    context = {
        'indicator_name': '2m Air Temperature (Kelvin)',
        'description': 'ERA5-Land daily mean temperature. Average over selected date range.',
        'center_lat': get_country_centroid()['lat'],
        'center_lng': get_country_centroid()['lng'],
        'default_start': "2024-02-01",
        'default_end': "2024-02-02",
    }
    return render(request, 'indicators/indicator_map.html', context)

# ========== RAINFALL  VIEW ==========

def rainfall_map(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        try:
            image = get_rainfall(start_date, end_date)
            # CHIRPS precipitation is in mm/day; typical range 0-50mm (adjust as needed)
            vis_params = {"min": 0, "max": 20, "palette": ["white", "lightblue", "blue", "darkblue"]}
            tile_url = _get_tile_url(image, vis_params)
            return JsonResponse({"tile_url": tile_url})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    context = {
        'indicator_name': 'Rainfall (Daily Precipitation)',
        'description': 'CHIRPS daily precipitation, mm/day. Average over selected date range.',
        'center_lat': get_country_centroid()['lat'],
        'center_lng': get_country_centroid()['lng'],
        'default_start': "2024-01-01",
        'default_end': "2024-01-31",
    }
    return render(request, 'indicators/indicator_map.html', context)