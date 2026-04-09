from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    path('indicators/', include('apps.indicators.urls')),
    path('viewer/', include('apps.ndvi_viewer.urls')),
    path('', TemplateView.as_view(template_name='map.html'), name='map'),

]