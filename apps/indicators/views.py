import ee
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta

# Helper: Zimbabwe boundary from FAO GAUL 2015 (reliable asset)
def get_zimbabwe_boundary():
    return (
        ee.FeatureCollection("FAO/GAUL/2015/level0")
        .filter(ee.Filter.eq("ADM0_NAME", "Malawi"))
        .geometry()
    )

def get_country_centroid():
    bounds = get_zimbabwe_boundary()
    centroid = bounds.centroid().coordinates().getInfo()
    return {'lat': centroid[1], 'lng': centroid[0]}

def _get_default_date():
    """Return a date string that definitely has MODIS data (e.g., 2024-02-01)."""
    return "2024-02-01"

# ========== NDVI (MODIS 16-day composite) ==========
def ndvi_map(request):
    # AJAX request: return tile URL for a given date
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        date = request.GET.get('date')
        if not date:
            return JsonResponse({'error': 'Missing date parameter'}, status=400)
        try:
            # Use the exact working logic from your code
            zimbabwe = get_zimbabwe_boundary()
            image = (
                ee.ImageCollection("MODIS/061/MOD13A2")
                .filterDate(date, ee.Date(date).advance(16, "day"))
                .select("NDVI")
                .mean()
                .multiply(0.0001)
                .clip(zimbabwe)
            )
            vis_params = {"min": 0, "max": 1, "palette": ["brown", "yellow", "green"]}
            map_id = image.getMapId(vis_params)
            return JsonResponse({"tile_url": map_id["tile_fetcher"].url_format})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # Normal page load
    default_date = _get_default_date()
    context = {
        'indicator_name': 'NDVI (Normalized Difference Vegetation Index)',
        'description': 'MODIS 16-day composite, 1km resolution. Values 0–1 (vegetation density).',
        'center_lat': get_country_centroid()['lat'],
        'center_lng': get_country_centroid()['lng'],
        'default_date': default_date,
    }
    return render(request, 'indicators/indicator_map.html', context)

# ========== Soil Moisture (ERA5-Land daily) ==========
def soil_moisture_map(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        date = request.GET.get('date')
        if not date:
            return JsonResponse({'error': 'Missing date parameter'}, status=400)
        try:
            zimbabwe = get_zimbabwe_boundary()
            # Soil moisture from ERA5-Land (volumetric soil water layer 1)
            image = (
                ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
                .filterDate(date, ee.Date(date).advance(1, "day"))
                .select("volumetric_soil_water_layer_1")
                .mean()
                .clip(zimbabwe)
            )
            vis_params = {"min": 0, "max": 0.5, "palette": ["brown", "orange", "lightblue", "blue"]}
            map_id = image.getMapId(vis_params)
            return JsonResponse({"tile_url": map_id["tile_fetcher"].url_format})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    context = {
        'indicator_name': 'Soil Moisture (Volumetric Water)',
        'description': 'ERA5-Land daily average, 0–0.5 m³/m³.',
        'center_lat': get_country_centroid()['lat'],
        'center_lng': get_country_centroid()['lng'],
        'default_date': _get_default_date(),
    }
    return render(request, 'indicators/indicator_map.html', context)

# ========== Temperature (ERA5-Land 2m air temperature) ==========
def temperature_map(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        date = request.GET.get('date')
        if not date:
            return JsonResponse({'error': 'Missing date parameter'}, status=400)
        try:
            zimbabwe = get_zimbabwe_boundary()
            image = (
                ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
                .filterDate(date, ee.Date(date).advance(1, "day"))
                .select("temperature_2m")
                .mean()
                .clip(zimbabwe)
            )
            vis_params = {"min": 290, "max": 310, "palette": ["blue", "yellow", "red"]}
            map_id = image.getMapId(vis_params)
            return JsonResponse({"tile_url": map_id["tile_fetcher"].url_format})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    context = {
        'indicator_name': '2m Air Temperature (Kelvin)',
        'description': 'ERA5-Land daily mean temperature (290K ≈ 17°C, 310K ≈ 37°C).',
        'center_lat': get_country_centroid()['lat'],
        'center_lng': get_country_centroid()['lng'],
        'default_date': _get_default_date(),
    }
    return render(request, 'indicators/indicator_map.html', context)