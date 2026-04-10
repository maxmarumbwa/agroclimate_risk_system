import ee

def get_soil_moisture(start_date, end_date):
    """
    Return EE Image (volumetric soil water layer 1, average over range).
    """
    from .boundary_utils import get_zimbabwe_boundary
    boundary = get_zimbabwe_boundary()
    
    collection = (
        ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
        .filterDate(start_date, end_date)
        .select("volumetric_soil_water_layer_1")
    )
    size = collection.size().getInfo()
    if size == 0:
        raise ValueError(f"No soil moisture data found from {start_date} to {end_date}")
    
    image = collection.mean().clip(boundary)
    return image