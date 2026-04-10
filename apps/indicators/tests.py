# apps/indicators/spi.py

import ee
from apps.gee.boundary_utils import get_country_boundary

def compute_spi(start_date, end_date, country="Zimbabwe"):
    """
    Compute a simplified SPI for the given period.
    SPI = (P - P_mean) / P_std
    where mean and std are derived from the same calendar period over historical years.
    """
    boundary = get_country_boundary(country)
    
    # Get rainfall for target period
    from apps.gee.rainfall import get_rainfall
    rainfall_target = get_rainfall(start_date, end_date, country)
    
    # Historical period (e.g., 1981-2023 for CHIRPS)
    hist_start = ee.Date('1981-01-01')
    hist_end = ee.Date('2023-12-31')
    
    collection = (ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
                  .filterDate(hist_start, hist_end)
                  .select("precipitation"))
    
    # Same calendar range as target
    start_md = ee.Date(start_date).getRelative('day', 'year')
    end_md = ee.Date(end_date).getRelative('day', 'year')
    filtered = collection.filter(ee.Filter.calendarRange(start_md, end_md, 'day_of_year'))
    
    # Compute mean and standard deviation
    mean_rain = filtered.mean().clip(boundary)
    std_rain = filtered.reduce(ee.Reducer.stdDev()).clip(boundary)
    
    # SPI = (P - mean) / std
    spi = rainfall_target.subtract(mean_rain).divide(std_rain)
    return spi