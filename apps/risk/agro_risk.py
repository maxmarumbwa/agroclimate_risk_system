import ee

def compute_agro_risk(vci, spi, temp, soil_moisture):
    """
    Compute AgroRisk index (0-1).
    Weights: VCI (40%), SPI (30%), temperature (20%), soil moisture (10%).
    """
    vci_norm = vci.divide(100)               # VCI is already 0-100
    vci_risk = ee.Image(1).subtract(vci_norm)

    spi_norm = spi.unitScale(-2, 2)          # assume SPI range -2..2
    temp_norm = temp.unitScale(290, 320)     # 290K = 17°C, 320K = 47°C
    soil_norm = soil_moisture.unitScale(0, 1)

    risk = (
        vci_risk.multiply(0.4)
        .add(spi_norm.multiply(0.3))
        .add(temp_norm.multiply(0.2))
        .add(soil_norm.multiply(0.1))
    )
    return risk.clamp(0, 1)