from rest_framework import serializers
from .models import SensorData, Threshold

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ['id', 'sensor_type', 'value', 'status', 'created_at']

class ThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threshold
        fields = ['sensor_type', 'warning_min', 'warning_max', 'danger_min', 'danger_max']

class SensorStatsSerializer(serializers.Serializer):
    sensor_type = serializers.CharField()
    avg = serializers.FloatField()
    min = serializers.FloatField()
    max = serializers.FloatField()
    count = serializers.IntegerField()

class AlertSerializer(serializers.Serializer):
    sensor_type = serializers.CharField()
    value = serializers.FloatField()
    status = serializers.CharField()
    message = serializers.CharField()
    created_at = serializers.DateTimeField()