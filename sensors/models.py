from django.db import models

class SensorData(models.Model):
    SENSOR_TYPES = [
        ('temperature', 'Temperature'),
        ('humidity', 'Humidity'),
        ('meat_status', 'Meat Status'),
    ]
    
    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('warning', 'Warning'),
        ('danger', 'Danger'),
    ]
    
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    value = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sensor_type}: {self.value} ({self.status})"

class Threshold(models.Model):
    sensor_type = models.CharField(max_length=20, unique=True)
    warning_min = models.FloatField(default=0)
    warning_max = models.FloatField(default=100)
    danger_min = models.FloatField(default=0)
    danger_max = models.FloatField(default=200)
    
    def __str__(self):
        return f"{self.sensor_type} thresholds"