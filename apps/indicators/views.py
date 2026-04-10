import ee
from django.shortcuts import render
from django.http import JsonResponse
from apps.gee.boundary_utils import get_country_centroid
from apps.gee.ndvi import get_ndvi
from apps.gee.soil_moisture import get_soil_moisture
from apps.gee.temperature import get_temperature
from apps.gee.rainfall import get_rainfall 

def _get_tile_url(image, vis_params):
    map_id = image.getMapId(vis_params)
    return map_id["tile_fetcher"].url_format

# ========== NDVI VIEW ==========
def ndvi_map(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    country = request.GET.get('country', 'Zimbabwe')
    
    if start_date and end_date:
        try:
            image = get_ndvi(start_date, end_date, country)
            vis_params = {"min": 0, "max": 1, "palette": ["brown", "yellow", "green"]}
            tile_url = _get_tile_url(image, vis_params)
            return JsonResponse({"tile_url": tile_url})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    centroid = get_country_centroid(country)
    context = {
        'indicator_name': 'NDVI (Normalized Difference Vegetation Index)',
        'description': 'MODIS 16-day composite, 1km resolution. Average over selected date range.',
        'center_lat': centroid['lat'],
        'center_lng': centroid['lng'],
        'default_start': "2024-02-01",
        'default_end': "2024-02-16",
        'legend_min': 0,
        'legend_max': 1,
        'legend_palette': ["brown", "yellow", "green"],
        'selected_country': country,
    }
    return render(request, 'indicators/indicator_map.html', context)

# ========== SOIL MOISTURE VIEW ==========
def soil_moisture_map(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    country = request.GET.get('country', 'Zimbabwe')
    
    if start_date and end_date:
        try:
            image = get_soil_moisture(start_date, end_date, country)
            vis_params = {"min": 0, "max": 0.5, "palette": ["brown", "orange", "lightblue", "blue"]}
            tile_url = _get_tile_url(image, vis_params)
            return JsonResponse({"tile_url": tile_url})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    centroid = get_country_centroid(country)
    context = {
        'indicator_name': 'Soil Moisture (Volumetric Water)',
        'description': 'ERA5-Land daily average, 0–0.5 m³/m³. Average over selected date range.',
        'center_lat': centroid['lat'],
        'center_lng': centroid['lng'],
        'default_start': "2024-02-01",
        'default_end': "2024-02-02",
        'legend_min': 0,
        'legend_max': 0.5,
        'legend_palette': ["brown", "orange", "lightblue", "blue"],
        'selected_country': country,
    }
    return render(request, 'indicators/indicator_map.html', context)

# ========== TEMPERATURE VIEW ==========
def temperature_map(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    country = request.GET.get('country', 'Zimbabwe')
    
    if start_date and end_date:
        try:
            image = get_temperature(start_date, end_date, country)
            vis_params = {"min": 290, "max": 310, "palette": ["blue", "yellow", "red"]}
            tile_url = _get_tile_url(image, vis_params)
            return JsonResponse({"tile_url": tile_url})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    centroid = get_country_centroid(country)
    context = {
        'indicator_name': '2m Air Temperature (Kelvin)',
        'description': 'ERA5-Land daily mean temperature. Average over selected date range.',
        'center_lat': centroid['lat'],
        'center_lng': centroid['lng'],
        'default_start': "2024-02-01",
        'default_end': "2024-02-02",
        'legend_min': 290,
        'legend_max': 310,
        'legend_palette': ["blue", "yellow", "red"],
        'selected_country': country,
    }
    return render(request, 'indicators/indicator_map.html', context)

# ========== RAINFALL VIEW ==========
def rainfall_map(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    country = request.GET.get('country', 'Zimbabwe')
    
    if start_date and end_date:
        try:
            image = get_rainfall(start_date, end_date, country)
            vis_params = {"min": 0, "max": 20, "palette": ["white", "lightblue", "blue", "darkblue"]}
            tile_url = _get_tile_url(image, vis_params)
            return JsonResponse({"tile_url": tile_url})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    centroid = get_country_centroid(country)
    context = {
        'indicator_name': 'Rainfall (Daily Precipitation)',
        'description': 'CHIRPS daily precipitation, mm/day. Average over selected date range.',
        'center_lat': centroid['lat'],
        'center_lng': centroid['lng'],
        'default_start': "2024-01-01",
        'default_end': "2024-01-31",
        'legend_min': 0,
        'legend_max': 20,
        'legend_palette': ["white", "lightblue", "blue", "darkblue"],
        'selected_country': country,
    }
    return render(request, 'indicators/indicator_map.html', context)