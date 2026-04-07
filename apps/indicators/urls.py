from django.urls import path
from . import views

urlpatterns = [
    path('rainfall/', views.rainfall_raster),
]