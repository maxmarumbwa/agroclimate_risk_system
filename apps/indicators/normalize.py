import ee

def normalize(image, min_val, max_val):
    """Linear normalisation to [0,1]."""
    return image.subtract(min_val).divide(max_val - min_val)