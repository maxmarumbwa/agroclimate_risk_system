# apps/gee/boundary_utils.py

import ee
from django.core.cache import cache  # optional, remove if not using cache

def get_all_countries(use_cache=True):
    """
    Return a sorted list of all ADM0_NAME values from the FAO/GAUL dataset.
    Uses Django cache to avoid repeated EE calls.
    """
    cache_key = "fao_gaul_country_list"
    if use_cache:
        countries = cache.get(cache_key)
        if countries:
            return countries
    
    fc = ee.FeatureCollection("FAO/GAUL/2015/level0")
    names = fc.aggregate_array("ADM0_NAME").getInfo()
    countries = sorted(set(names))
    
    if use_cache:
        cache.set(cache_key, countries, 86400)  # 24 hours
    return countries

def get_country_boundary(country_name="Zimbabwe"):
    """
    Return EE geometry for a given country name.
    Raises ValueError if country not found.
    """
    fc = ee.FeatureCollection("FAO/GAUL/2015/level0").filter(ee.Filter.eq("ADM0_NAME", country_name))
    size = fc.size().getInfo()
    if size == 0:
        raise ValueError(f"Country '{country_name}' not found in GAUL dataset.")
    return fc.geometry()

def get_country_centroid(country_name="Zimbabwe"):
    """
    Return {'lat': x, 'lng': y} for the given country.
    """
    bounds = get_country_boundary(country_name)
    centroid = bounds.centroid().coordinates().getInfo()
    return {'lat': centroid[1], 'lng': centroid[0]}

# Legacy functions (optional, for backward compatibility)
def get_zimbabwe_boundary():
    return get_country_boundary("Zimbabwe")

def get_zimbabwe_centroid():
    return get_country_centroid("Zimbabwe")