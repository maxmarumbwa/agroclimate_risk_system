import ee

def get_rainfall(start_date, end_date):
    """Return total rainfall (mm) from CHIRPS daily."""
    return ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY") \
        .filterDate(start_date, end_date) \
        .sum()