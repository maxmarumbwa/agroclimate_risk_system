import ee

def get_temperature(start_date, end_date):
    """Return mean 2m air temperature (K) from ERA5-Land daily."""
    return ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR") \
        .filterDate(start_date, end_date) \
        .select("temperature_2m") \
        .mean()