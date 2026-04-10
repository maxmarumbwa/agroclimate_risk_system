from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('ndvi/', views.ndvi_map, name='ndvi_map'),
    path('soil-moisture/', views.soil_moisture_map, name='soil_moisture_map'),
    path('temperature/', views.temperature_map, name='temperature_map'),
    path('rainfall/', views.rainfall_map, name='rainfall_map'),
]