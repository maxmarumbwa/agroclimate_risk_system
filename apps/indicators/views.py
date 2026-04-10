import ee
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime

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

# ========== NDVI ==========
def ndvi_map(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # If both dates are provided, return tile JSON (AJAX call)
    if start_date and end_date:
        try:
            zimbabwe = get_zimbabwe_boundary()
            # Simple filtering: get collection over the range, mean, then scale
            collection = ee.ImageCollection("MODIS/061/MOD13A2") \
                .filterDate(start_date, end_date) \
                .select("NDVI")
            
            if collection.size().getInfo() == 0:
                return JsonResponse({'error': 'No data for this period'}, status=404)
            
            image = collection.mean().multiply(0.0001).clip(zimbabwe)
            vis_params = {"min": 0, "max": 1, "palette": ["brown", "yellow", "green"]}
            map_id = image.getMapId(vis_params)
            return JsonResponse({"tile_url": map_id["tile_fetcher"].url_format})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # Otherwise render the HTML template with default dates
    default_start = "2024-02-01"
    default_end = "2024-02-16"
    context = {
        'indicator_name': 'NDVI (Normalized Difference Vegetation Index)',
        'description': 'MODIS 16-day composite, 1km resolution. Average over selected date range.',
        'center_lat': get_country_centroid()['lat'],
        'center_lng': get_country_centroid()['lng'],
        'default_start': default_start,
        'default_end': default_end,
    }
    return render(request, 'indicators/indicator_map.html', context)

# ========== Soil Moisture ==========
def soil_moisture_map(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        try:
            zimbabwe = get_zimbabwe_boundary()
            collection = ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR") \
                .filterDate(start_date, end_date) \
                .select("volumetric_soil_water_layer_1")
            
            if collection.size().getInfo() == 0:
                return JsonResponse({'error': 'No soil moisture data for this period'}, status=404)
            
            image = collection.mean().clip(zimbabwe)
            vis_params = {"min": 0, "max": 0.5, "palette": ["brown", "orange", "lightblue", "blue"]}
            map_id = image.getMapId(vis_params)
            return JsonResponse({"tile_url": map_id["tile_fetcher"].url_format})
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

# ========== Temperature ==========
def temperature_map(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        try:
            zimbabwe = get_zimbabwe_boundary()
            collection = ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR") \
                .filterDate(start_date, end_date) \
                .select("temperature_2m")
            
            if collection.size().getInfo() == 0:
                return JsonResponse({'error': 'No temperature data for this period'}, status=404)
            
            image = collection.mean().clip(zimbabwe)
            vis_params = {"min": 290, "max": 310, "palette": ["blue", "yellow", "red"]}
            map_id = image.getMapId(vis_params)
            return JsonResponse({"tile_url": map_id["tile_fetcher"].url_format})
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