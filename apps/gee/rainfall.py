import ee
from .boundary_utils import get_country_boundary

def get_rainfall(start_date, end_date, country="Zimbabwe"):
    """
    Return EE Image (daily precipitation, average over range).
    Uses CHIRPS daily dataset.
    """
    boundary = get_country_boundary(country)
    
    collection = (
        ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
        .filterDate(start_date, end_date)
        .select("precipitation")
    )
    size = collection.size().getInfo()
    if size == 0:
        raise ValueError(f"No rainfall data found from {start_date} to {end_date}")
    
    image = collection.mean().clip(boundary)
    return image