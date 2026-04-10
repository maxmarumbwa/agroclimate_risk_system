import ee
from .boundary_utils import get_country_boundary

def get_temperature(start_date, end_date, country="Zimbabwe"):
    """
    Return EE Image (2m air temperature, average over range).
    """
    boundary = get_country_boundary(country)
    
    collection = (
        ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
        .filterDate(start_date, end_date)
        .select("temperature_2m")
    )
    size = collection.size().getInfo()
    if size == 0:
        raise ValueError(f"No temperature data found from {start_date} to {end_date}")
    
    image = collection.mean().clip(boundary)
    return image