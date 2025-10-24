from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/sensor-data/', views.get_sensor_data, name='sensor-data'),
]
