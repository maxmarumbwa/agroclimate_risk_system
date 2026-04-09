import ee

def get_ndvi(start_date, end_date):
    """Return mean NDVI image for date range (MODIS MOD13Q1)."""
    collection = ee.ImageCollection("MODIS/006/MOD13A2") \
        .filterDate(start_date, end_date) \
        .select("NDVI")
    ndvi = collection.mean().multiply(0.0001)
    return ndvi

