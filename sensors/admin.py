from django.contrib import admin
from .models import SensorData, Threshold

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ['sensor_type', 'value', 'status', 'created_at']
    list_filter = ['sensor_type', 'status', 'created_at']
    search_fields = ['sensor_type']
    ordering = ['-created_at']

@admin.register(Threshold)
class ThresholdAdmin(admin.ModelAdmin):
    list_display = ['sensor_type', 'warning_min', 'warning_max', 'danger_min', 'danger_max']