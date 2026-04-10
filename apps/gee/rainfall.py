import ee
def get_rainfall(start_date, end_date):
    """
    Return EE Image (daily precipitation, average over range).
    Uses CHIRPS daily dataset.
    """
    from .boundary_utils import get_zimbabwe_boundary
    boundary = get_zimbabwe_boundary()
    
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