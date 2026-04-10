import ee

def get_ndvi(start_date, end_date):
    """
    Return an EE Image (NDVI averaged over date range, scaled 0-1).
    Raises ValueError if no data found.
    """

    from .boundary_utils import get_zimbabwe_boundary
    boundary = get_zimbabwe_boundary()
    
    collection = (
        ee.ImageCollection("MODIS/061/MOD13A2")
        .filterDate(start_date, end_date)
        .select("NDVI")
    )
    size = collection.size().getInfo()
    if size == 0:
        raise ValueError(f"No NDVI data found from {start_date} to {end_date}")
    
    # Mean then scale
    image = collection.mean().multiply(0.0001).clip(boundary)
    return image