from django.urls import path
from . import views

urlpatterns = [
    path('sensors/', views.sensor_data_view, name='sensor-list-create'),
    path('sensors/latest/', views.latest_sensor_data, name='sensor-latest'),
    path('sensors/stats/', views.sensor_stats, name='sensor-stats'),
    path('settings/threshold/', views.update_threshold, name='update-threshold'),
    path('alerts/', views.alerts, name='alerts'),
]