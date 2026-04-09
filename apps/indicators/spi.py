import ee

def compute_spi(rainfall, mean_rainfall, std_dev):
    """Standardised Precipitation Index (simplified)."""
    return rainfall.subtract(mean_rainfall).divide(std_dev)