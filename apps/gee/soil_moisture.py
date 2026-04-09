import ee

def get_soil_moisture(start_date, end_date):
    """Return mean volumetric soil water (0-1) from ERA5-Land."""
    return ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR") \
        .filterDate(start_date, end_date) \
        .select("volumetric_soil_water_layer_1") \
        .mean()