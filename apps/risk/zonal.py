import ee

def zonal_risk(risk_image, geometry, scale=250):
    """Return mean risk value over a given geometry."""
    stats = risk_image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=scale,
        bestEffort=True
    )
    return stats.getInfo()