# apps/indicators/normalize.py

import ee

def normalize(image, min_val, max_val):
    """
    Linearly scale an EE image to 0-1 range.
    Values below min become 0, above max become 1.
    """
    return image.subtract(min_val).divide(max_val - min_val).clamp(0, 1)