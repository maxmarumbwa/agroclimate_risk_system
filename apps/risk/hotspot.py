import ee

def get_hotspots(risk_image, threshold=0.75):
    """Return binary image (1 where risk > threshold)."""
    return risk_image.gt(threshold)