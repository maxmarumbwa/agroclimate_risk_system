import ee

def compute_vci(ndvi, ndvi_min, ndvi_max):
    """Vegetation Condition Index (0-100)."""
    return ndvi.subtract(ndvi_min) \
               .divide(ndvi_max.subtract(ndvi_min)) \
               .multiply(100)