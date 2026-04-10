import ee
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta

# Helper: Zimbabwe boundary from FAO GAUL 2015 (reliable asset)
def get_zimbabwe_boundary():
    return (
        ee.FeatureCollection("FAO/GAUL/2015/level0")
        .filter(ee.Filter.eq("ADM0_NAME", "Zimbabwe"))
        .geometry()
    )

def get_country_centroid():
    bounds = get_zimbabwe_boundary()
    centroid = bounds.centroid().coordinates().getInfo()
    return {'lat': centroid[1], 'lng': centroid[0]}

def _get_default_start_end(indicator_type):
    """Return default start and end dates based on indicator type."""
    if indicator_type == 'ndvi':
        # NDVI 16-day composite - show a typical 16-day period
        return "2024-02-01", "2024-02-16"
    else:
        # Daily indicators - show a single day range
        return "2024-02-01", "2024-02-02"

# ========== NDVI (MODIS 16-day composite) ==========
def ndvi_map(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if not start_date or not end_date:
            return JsonResponse({'error': 'Missing start_date or end_date parameter'}, status=400)
        try:
            zimbabwe = get_zimbabwe_boundary()
            collection = (
                ee.ImageCollection("MODIS/061/MOD13A2")
                .filterDate(start_date, end_date)
                .select("NDVI")
                .map(lambda img: img.multiply(0.0001))
            )
            # Compute mean over the date range
            image = collection.mean().clip(zimbabwe)
            # Check if collection was empty
            if not collection.size().getInfo():
                return JsonResponse({'error': f'No MODIS data found for dates {start_date} to {end_date}'}, status=404)
            
            vis_params = {"min": 0, "max": 1, "palette": ["brown", "yellow", "green"]}
            map_id = image.getMapId(vis_params)
            return JsonResponse({"tile_url": map_id["tile_fetcher"].url_format})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    default_start, default_end = _get_default_start_end('ndvi')
    context = {
        'indicator_name': 'NDVI (Normalized Difference Vegetation Index)',
        'description': 'MODIS 16-day composite, 1km resolution. Values 0–1 (vegetation density). Shown as average over selected date range.',
        'center_lat': get_country_centroid()['lat'],
        'center_lng': get_country_centroid()['lng'],
        'default_start': default_start,
        'default_end': default_end,
    }
    return render(request, 'indicators/indicator_map.html', context)

# ========== Soil Moisture (ERA5-Land daily) ==========
def soil_moisture_map(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if not start_date or not end_date:
            return JsonResponse({'error': 'Missing start_date or end_date parameter'}, status=400)
        try:
            zimbabwe = get_zimbabwe_boundary()
            collection = (
                ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
                .filterDate(start_date, end_date)
                .select("volumetric_soil_water_layer_1")
            )
            if collection.size().getInfo() == 0:
                return JsonResponse({'error': f'No soil moisture data found for dates {start_date} to {end_date}'}, status=404)
            
            image = collection.mean().clip(zimbabwe)
            vis_params = {"min": 0, "max": 0.5, "palette": ["brown", "orange", "lightblue", "blue"]}
            map_id = image.getMapId(vis_params)
            return JsonResponse({"tile_url": map_id["tile_fetcher"].url_format})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    default_start, default_end = _get_default_start_end('soil')
    context = {
        'indicator_name': 'Soil Moisture (Volumetric Water)',
        'description': 'ERA5-Land daily average, 0–0.5 m³/m³. Shown as average over selected date range.',
        'center_lat': get_country_centroid()['lat'],
        'center_lng': get_country_centroid()['lng'],
        'default_start': default_start,
        'default_end': default_end,
    }
    return render(request, 'indicators/indicator_map.html', context)

# ========== Temperature (ERA5-Land 2m air temperature) ==========
def temperature_map(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if not start_date or not end_date:
            return JsonResponse({'error': 'Missing start_date or end_date parameter'}, status=400)
        try:
            zimbabwe = get_zimbabwe_boundary()
            collection = (
                ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
                .filterDate(start_date, end_date)
                .select("temperature_2m")
            )
            if collection.size().getInfo() == 0:
                return JsonResponse({'error': f'No temperature data found for dates {start_date} to {end_date}'}, status=404)
            
            image = collection.mean().clip(zimbabwe)
            vis_params = {"min": 290, "max": 310, "palette": ["blue", "yellow", "red"]}
            map_id = image.getMapId(vis_params)
            return JsonResponse({"tile_url": map_id["tile_fetcher"].url_format})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    default_start, default_end = _get_default_start_end('temperature')
    context = {
        'indicator_name': '2m Air Temperature (Kelvin)',
        'description': 'ERA5-Land daily mean temperature (290K ≈ 17°C, 310K ≈ 37°C). Shown as average over selected date range.',
        'center_lat': get_country_centroid()['lat'],
        'center_lng': get_country_centroid()['lng'],
        'default_start': default_start,
        'default_end': default_end,
    }
    return render(request, 'indicators/indicator_map.html', context)