import ee

def get_zimbabwe_boundary():
    """Return the EE geometry for Zimbabwe."""
    return (
        ee.FeatureCollection("FAO/GAUL/2015/level0")
        .filter(ee.Filter.eq("ADM0_NAME", "Zimbabwe"))
        .geometry()
    )

def get_country_centroid():
    """Return {'lat': x, 'lng': y} for Zimbabwe."""
    bounds = get_zimbabwe_boundary()
    centroid = bounds.centroid().coordinates().getInfo()
    return {'lat': centroid[1], 'lng': centroid[0]}