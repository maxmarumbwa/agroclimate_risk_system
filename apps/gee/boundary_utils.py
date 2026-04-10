import ee

def get_country_boundary(country_name="Zimbabwe"):
    """
    Return the EE geometry for a given country name.
    Uses FAO/GAUL 2015 level 0 dataset.
    """
    return (
        ee.FeatureCollection("FAO/GAUL/2015/level0")
        .filter(ee.Filter.eq("ADM0_NAME", country_name))
        .geometry()
    )

def get_country_centroid(country_name="Zimbabwe"):
    """
    Return {'lat': x, 'lng': y} for the given country.
    """
    bounds = get_country_boundary(country_name)
    centroid = bounds.centroid().coordinates().getInfo()
    return {'lat': centroid[1], 'lng': centroid[0]}

# Keep old function names for backward compatibility if needed
def get_zimbabwe_boundary():
    return get_country_boundary("Zimbabwe")

def get_zimbabwe_centroid():
    return get_country_centroid("Zimbabwe")