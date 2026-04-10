# apps/indicators/vci.py

import ee
from apps.gee.boundary_utils import get_country_boundary

def compute_vci(start_date, end_date, country="Zimbabwe"):
    boundary = get_country_boundary(country)
    
    # Get NDVI for target period
    ndvi_target = get_ndvi_for_period(start_date, end_date, country)
    
    # Historical period (MODIS from 2000)
    hist_start = ee.Date('2000-01-01')
    hist_end = ee.Date('2023-12-31')
    
    collection = (ee.ImageCollection("MODIS/061/MOD13A2")
                  .filterDate(hist_start, hist_end)
                  .select("NDVI")
                  .map(lambda img: img.multiply(0.0001)))
    
    # Filter by same calendar range (month-day)
    start_md = ee.Date(start_date).getRelative('day', 'year')
    end_md = ee.Date(end_date).getRelative('day', 'year')
    filtered = collection.filter(ee.Filter.calendarRange(start_md, end_md, 'day_of_year'))
    
    # Check if empty
    size = filtered.size().getInfo()
    if size == 0:
        raise ValueError(f"No historical NDVI data for {country} in this date range")
    
    ndvi_min = filtered.min().clip(boundary)
    ndvi_max = filtered.max().clip(boundary)
    
    # Avoid division by zero
    denominator = ndvi_max.subtract(ndvi_min).max(0.001)
    vci = ndvi_target.subtract(ndvi_min).divide(denominator).multiply(100).clamp(0, 100)
    return vci

def get_ndvi_for_period(start_date, end_date, country):
    from apps.gee.ndvi import get_ndvi
    return get_ndvi(start_date, end_date, country)