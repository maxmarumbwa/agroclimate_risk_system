import ee

def get_zimbabwe_boundary():
    """Return an ee.Geometry for Zimbabwe using FAO GAUL dataset."""
    # Load GAUL Level 0 (country boundaries)
    gaul0 = ee.FeatureCollection("projects/sat-io/open-datasets/FAO/GAUL/GAUL_2024_L0")
    # Filter for Zimbabwe (ISO3 code 'ZWE')
    zimbabwe = gaul0.filter(ee.Filter.eq('iso3_code', 'ZWE')).geometry()
    return zimbabwe

def get_country_centroid(country_iso3='ZWE'):
    """Return centroid coordinates for a country."""
    gaul0 = ee.FeatureCollection("projects/sat-io/open-datasets/FAO/GAUL/GAUL_2024_L0")
    country = gaul0.filter(ee.Filter.eq('iso3_code', country_iso3))
    centroid = country.geometry().centroid().coordinates().getInfo()
    return {'lat': centroid[1], 'lng': centroid[0]}
