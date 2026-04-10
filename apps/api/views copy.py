import ee
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from apps.gee.ndvi import get_ndvi
from apps.gee.rainfall import get_rainfall
from apps.gee.temperature import get_temperature
from apps.gee.soil_moisture import get_soil_moisture
from apps.indicators.vci import compute_vci
from apps.indicators.spi import compute_spi
from apps.risk.agro_risk import compute_agro_risk
from apps.risk.zonal import zonal_risk

# Helper: get long-term NDVI min/max for VCI (example using a 5-year reference)
def get_ndvi_reference(region, start_ref, end_ref):
    ref_coll = ee.ImageCollection("MODIS/006/MOD13Q1") \
        .filterDate(start_ref, end_ref) \
        .select("NDVI") \
        .map(lambda img: img.multiply(0.0001))
    ndvi_min = ref_coll.min()
    ndvi_max = ref_coll.max()
    return ndvi_min, ndvi_max

@csrf_exempt
@require_http_methods(["GET"])
def agro_risk_map(request):
    """Return a tile URL for the AgroRisk map (Leaflet)."""
    start = request.GET.get("start_date")
    end = request.GET.get("end_date")
    if not start or not end:
        return JsonResponse({"error": "start_date and end_date required"}, status=400)

    # 1. Fetch raw data
    ndvi = get_ndvi(start, end)
    rainfall = get_rainfall(start, end)
    temp = get_temperature(start, end)
    soil = get_soil_moisture(start, end)

    # 2. Compute VCI using a reference period (e.g., 2019-2023)
    # For demo, we use a fixed region (India) and hardcoded reference dates.
    india = ee.Geometry.Rectangle([68.0, 6.0, 97.0, 36.0])
    ndvi_min, ndvi_max = get_ndvi_reference(india, '2019-01-01', '2023-12-31')
    vci = compute_vci(ndvi, ndvi_min, ndvi_max)

    # 3. Simplified SPI: use a fixed mean/std (real implementation would use historical)
    # Here we assume mean=300 mm, std=100 mm for the date range.
    mean_rain = ee.Image.constant(300)
    std_rain = ee.Image.constant(100)
    spi = compute_spi(rainfall, mean_rain, std_rain)

    # 4. Compute risk
    risk = compute_agro_risk(vci, spi, temp, soil)

    # 5. Get map ID for tile layer
    viz = {"min": 0, "max": 1, "palette": ["green", "yellow", "red"]}
    map_id = risk.getMapId(viz)

    return JsonResponse({
        "tile_url": map_id["tile_fetcher"].url_format,
        "min": 0,
        "max": 1
    })

@require_http_methods(["GET"])
def agro_risk_timeseries(request):
    """Return risk values for a point over a date range."""
    lat = float(request.GET.get("lat", 0))
    lon = float(request.GET.get("lon", 0))
    start = request.GET.get("start_date")
    end = request.GET.get("end_date")
    if not start or not end:
        return JsonResponse({"error": "start_date and end_date required"}, status=400)

    point = ee.Geometry.Point([lon, lat])
    # Generate list of dates (monthly steps for simplicity)
    from datetime import datetime, timedelta
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    dates = []
    current = start_dt
    while current <= end_dt:
        dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=30)  # monthly

    values = []
    for d in dates:
        # Compute risk for that month
        ndvi = get_ndvi(d, d)
        rainfall = get_rainfall(d, d)
        temp = get_temperature(d, d)
        soil = get_soil_moisture(d, d)
        # Simplified: reuse same reference as before
        india = ee.Geometry.Rectangle([68.0, 6.0, 97.0, 36.0])
        ndvi_min, ndvi_max = get_ndvi_reference(india, '2019-01-01', '2023-12-31')
        vci = compute_vci(ndvi, ndvi_min, ndvi_max)
        mean_rain = ee.Image.constant(300)
        std_rain = ee.Image.constant(100)
        spi = compute_spi(rainfall, mean_rain, std_rain)
        risk = compute_agro_risk(vci, spi, temp, soil)
        val = risk.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=250
        ).getInfo()
        values.append(val.get("constant", None))

    return JsonResponse({"dates": dates, "risk_values": values})

@require_http_methods(["GET"])
def zonal_stats(request):
    """Return mean risk for a district (GeoJSON polygon)."""
    # For simplicity, we accept a GeoJSON string
    import json
    geojson_str = request.GET.get("geometry")
    if not geojson_str:
        return JsonResponse({"error": "geometry parameter required"}, status=400)
    geojson = json.loads(geojson_str)
    geom = ee.Geometry(geojson)

    start = request.GET.get("start_date")
    end = request.GET.get("end_date")
    if not start or not end:
        return JsonResponse({"error": "start_date and end_date required"}, status=400)

    # Recompute risk for the given period (same as map)
    ndvi = get_ndvi(start, end)
    rainfall = get_rainfall(start, end)
    temp = get_temperature(start, end)
    soil = get_soil_moisture(start, end)
    india = ee.Geometry.Rectangle([68.0, 6.0, 97.0, 36.0])
    ndvi_min, ndvi_max = get_ndvi_reference(india, '2019-01-01', '2023-12-31')
    vci = compute_vci(ndvi, ndvi_min, ndvi_max)
    mean_rain = ee.Image.constant(300)
    std_rain = ee.Image.constant(100)
    spi = compute_spi(rainfall, mean_rain, std_rain)
    risk = compute_agro_risk(vci, spi, temp, soil)

    mean_risk = zonal_risk(risk, geom)
    return JsonResponse({"mean_risk": mean_risk})

@require_http_methods(["GET"])
def top_districts(request):
    """Return top 10 districts with highest risk (simplified: returns static list)."""
    # In production, you would iterate over district geometries and compute mean risk.
    # For demo, return dummy response.
    return JsonResponse({
        "top_districts": [
            {"name": "District A", "risk": 0.89},
            {"name": "District B", "risk": 0.85},
            {"name": "District C", "risk": 0.82}
        ]
    })