# apps/risk/agro_risk.py

import ee
from apps.indicators.normalize import normalize
from apps.indicators.vci import compute_vci
from apps.indicators.spi import compute_spi
from apps.gee.temperature import get_temperature
from apps.gee.soil_moisture import get_soil_moisture

def compute_agro_risk(start_date, end_date, country="Zimbabwe"):
    """
    Return a risk map (0-1, higher = more risk) based on:
    - VCI (inverted: low VCI = high risk)
    - SPI (negative = dry risk, positive = wet risk? We treat absolute deviation)
    - Temperature (normalised, high temp = risk)
    - Soil moisture (low = risk)
    """
    # VCI (0-100) -> convert to risk: 1 - (VCI/100)
    vci = compute_vci(start_date, end_date, country)
    vci_risk = ee.Image(1).subtract(vci.divide(100))
    
    # SPI: treat both negative and positive deviations as risk (absolute value)
    spi = compute_spi(start_date, end_date, country)
    # Clip SPI to [-2,2] and map to 0-1 (|SPI|/2)
    spi_risk = spi.abs().divide(2).clamp(0, 1)
    
    # Temperature: higher temp = higher risk (normalise between 290K and 320K)
    temp = get_temperature(start_date, end_date, country)
    temp_risk = normalize(temp, 290, 320)
    
    # Soil moisture: lower = higher risk (invert normalised value)
    soil = get_soil_moisture(start_date, end_date, country)
    soil_norm = normalize(soil, 0, 0.5)
    soil_risk = ee.Image(1).subtract(soil_norm)
    
    # Weighted combination (adjust weights as needed)
    risk = (vci_risk.multiply(0.4)
            .add(spi_risk.multiply(0.3))
            .add(temp_risk.multiply(0.2))
            .add(soil_risk.multiply(0.1)))
    
    return risk.clamp(0, 1)