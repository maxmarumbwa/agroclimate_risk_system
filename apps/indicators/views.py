# apps/gee/views.py

import ee
from django.shortcuts import render
from django.http import JsonResponse
from apps.gee.boundary_utils import get_country_centroid, get_all_countries  # <-- flat list
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
    
    try:
        centroid = get_country_centroid(country)
    except Exception:
        centroid = get_country_centroid("Zimbabwe")
        country = "Zimbabwe"
    
    countries_list = get_all_countries()
    
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
        'countries_list': countries_list,
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
    
    try:
        centroid = get_country_centroid(country)
    except Exception:
        centroid = get_country_centroid("Zimbabwe")
        country = "Zimbabwe"
    
    countries_list = get_all_countries()
    
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
        'countries_list': countries_list,
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
    
    try:
        centroid = get_country_centroid(country)
    except Exception:
        centroid = get_country_centroid("Zimbabwe")
        country = "Zimbabwe"
    
    countries_list = get_all_countries()
    
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
        'countries_list': countries_list,
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
    
    try:
        centroid = get_country_centroid(country)
    except Exception:
        centroid = get_country_centroid("Zimbabwe")
        country = "Zimbabwe"
    
    countries_list = get_all_countries()
    
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
        'countries_list': countries_list,
    }
    return render(request, 'indicators/indicator_map.html', context)

# ========== AGRO RISK VIEW ==========
from apps.risk.agro_risk import compute_agro_risk

def risk_map(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    country = request.GET.get('country', 'Zimbabwe')
    
    if start_date and end_date:
        try:
            risk_image = compute_agro_risk(start_date, end_date, country)
            vis_params = {"min": 0, "max": 1, "palette": ["green", "yellow", "orange", "red"]}
            tile_url = _get_tile_url(risk_image, vis_params)
            return JsonResponse({"tile_url": tile_url})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    try:
        centroid = get_country_centroid(country)
    except Exception:
        centroid = get_country_centroid("Zimbabwe")
        country = "Zimbabwe"
    
    countries_list = get_all_countries()   # <-- flat list
    
    context = {
        'indicator_name': 'Agro‑Risk Index (0 = low risk, 1 = high risk)',
        'description': 'Combines VCI, SPI, temperature, and soil moisture. Higher values indicate higher agricultural risk.',
        'center_lat': centroid['lat'],
        'center_lng': centroid['lng'],
        'default_start': "2024-02-01",
        'default_end': "2024-02-16",
        'legend_min': 0,
        'legend_max': 1,
        'legend_palette': ["green", "yellow", "orange", "red"],
        'selected_country': country,
        'countries_list': countries_list,   # <-- flat list
    }
    return render(request, 'indicators/indicator_map.html', context)

############ risnk layers ###############
# apps/gee/views.py (add after other views)

from apps.indicators.vci import compute_vci
from apps.indicators.spi import compute_spi
from apps.indicators.normalize import normalize
from apps.gee.temperature import get_temperature
from apps.gee.soil_moisture import get_soil_moisture

def index_map(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    country = request.GET.get('country', 'Zimbabwe')
    index = request.GET.get('index', 'vci')   # vci, spi, temp_norm, soil_norm

    if start_date and end_date:
        try:
            if index == 'vci':
                image = compute_vci(start_date, end_date, country)
                vis_params = {"min": 0, "max": 100, "palette": ["brown", "yellow", "green"]}
                legend_min, legend_max = 0, 100
                legend_palette = ["brown", "yellow", "green"]
                indicator_name = "VCI (Vegetation Condition Index)"
                description = "VCI = (NDVI - NDVI_min)/(NDVI_max - NDVI_min)*100. 0 = poor vegetation, 100 = excellent."
            elif index == 'spi':
                image = compute_spi(start_date, end_date, country)
                vis_params = {"min": -2, "max": 2, "palette": ["red", "white", "blue"]}
                legend_min, legend_max = -2, 2
                legend_palette = ["red", "white", "blue"]
                indicator_name = "SPI (Standardised Precipitation Index)"
                description = "SPI = (P - P_mean)/P_std. Negative = dry, positive = wet."
            elif index == 'temp_norm':
                temp = get_temperature(start_date, end_date, country)
                image = normalize(temp, 290, 320)
                vis_params = {"min": 0, "max": 1, "palette": ["blue", "yellow", "red"]}
                legend_min, legend_max = 0, 1
                legend_palette = ["blue", "yellow", "red"]
                indicator_name = "Normalized Temperature"
                description = "Temperature normalized between 290K and 320K. Higher = warmer."
            elif index == 'soil_norm':
                soil = get_soil_moisture(start_date, end_date, country)
                image = normalize(soil, 0, 0.5)
                vis_params = {"min": 0, "max": 1, "palette": ["brown", "lightblue", "blue"]}
                legend_min, legend_max = 0, 1
                legend_palette = ["brown", "lightblue", "blue"]
                indicator_name = "Normalized Soil Moisture"
                description = "Volumetric soil water normalized 0-1. Higher = wetter."
            else:
                raise ValueError(f"Unknown index: {index}")

            tile_url = _get_tile_url(image, vis_params)
            return JsonResponse({"tile_url": tile_url})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # GET request without dates → render the template
    try:
        centroid = get_country_centroid(country)
    except Exception:
        centroid = get_country_centroid("Zimbabwe")
        country = "Zimbabwe"

    countries_list = get_all_countries()

    # Default legend values (will be overridden by JS but used for initial render)
    if index == 'vci':
        legend_min, legend_max, legend_palette = 0, 100, ["brown", "yellow", "green"]
        indicator_name = "VCI (Vegetation Condition Index)"
        description = "VCI = (NDVI - NDVI_min)/(NDVI_max - NDVI_min)*100. 0 = poor vegetation, 100 = excellent."
    elif index == 'spi':
        legend_min, legend_max, legend_palette = -2, 2, ["red", "white", "blue"]
        indicator_name = "SPI (Standardised Precipitation Index)"
        description = "SPI = (P - P_mean)/P_std. Negative = dry, positive = wet."
    elif index == 'temp_norm':
        legend_min, legend_max, legend_palette = 0, 1, ["blue", "yellow", "red"]
        indicator_name = "Normalized Temperature"
        description = "Temperature normalized between 290K and 320K. Higher = warmer."
    elif index == 'soil_norm':
        legend_min, legend_max, legend_palette = 0, 1, ["brown", "lightblue", "blue"]
        indicator_name = "Normalized Soil Moisture"
        description = "Volumetric soil water normalized 0-1. Higher = wetter."
    else:
        legend_min, legend_max, legend_palette = 0, 1, ["gray"]
        indicator_name = "Unknown Index"

    context = {
        'indicator_name': indicator_name,
        'description': description,
        'center_lat': centroid['lat'],
        'center_lng': centroid['lng'],
        'default_start': "2024-02-01",
        'default_end': "2024-02-16",
        'legend_min': legend_min,
        'legend_max': legend_max,
        'legend_palette': legend_palette,
        'selected_country': country,
        'selected_index': index,
        'countries_list': countries_list,
    }
    return render(request, 'indicators/indices_map.html', context)