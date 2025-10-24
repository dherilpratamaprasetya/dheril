from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Avg, Min, Max, Count
from django.utils import timezone
from datetime import timedelta
import json
import random
from .models import SensorData, Threshold

def determine_status(sensor_type, value):
    """Determine sensor status based on value and thresholds"""
    if sensor_type == 'gas':
        if value > 400:
            return 'danger'
        elif value > 200:
            return 'warning'
        else:
            return 'normal'
    elif sensor_type == 'temperature':
        if value > 35:
            return 'warning'
        else:
            return 'normal'
    return 'normal'

def generate_dummy_sensor_data():
    """Generate dummy sensor data for self-monitoring"""
    # Generate gas data (100-600 ppm)
    gas_value = random.uniform(100, 600)
    gas_status = determine_status('gas', gas_value)

    gas_data = SensorData.objects.create(
        sensor_type='gas',
        value=round(gas_value, 2),
        status=gas_status
    )

    # Generate temperature data (20-40°C)
    temp_value = random.uniform(20, 40)
    temp_status = determine_status('temperature', temp_value)

    temp_data = SensorData.objects.create(
        sensor_type='temperature',
        value=round(temp_value, 2),
        status=temp_status
    )

    return gas_data, temp_data

def add_cors_headers(response):
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@csrf_exempt
@require_http_methods(["GET", "POST"])
def sensor_data_view(request):
    if request.method == 'GET':
        sensors = SensorData.objects.all().order_by('-created_at')[:20]
        data = []
        for sensor in sensors:
            data.append({
                'id': sensor.id,
                'sensor_type': sensor.sensor_type,
                'value': sensor.value,
                'status': sensor.status,
                'created_at': sensor.created_at.isoformat()
            })
        response = JsonResponse({'results': data})
        return add_cors_headers(response)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            sensor = SensorData.objects.create(
                sensor_type=data['sensor_type'],
                value=data['value'],
                status=data['status']
            )
            response = JsonResponse({
                'id': sensor.id,
                'sensor_type': sensor.sensor_type,
                'value': sensor.value,
                'status': sensor.status,
                'created_at': sensor.created_at.isoformat()
            })
            return add_cors_headers(response)
        except Exception as e:
            response = JsonResponse({'error': str(e)}, status=400)
            return add_cors_headers(response)

def latest_sensor_data(request):
    # Check if we have recent data (within last 5 seconds)
    now = timezone.now()
    five_seconds_ago = now - timedelta(seconds=5)

    gas_data = SensorData.objects.filter(sensor_type='gas').order_by('-created_at').first()
    temp_data = SensorData.objects.filter(sensor_type='temperature').order_by('-created_at').first()

    # If no data exists or data is older than 5 seconds, generate new dummy data
    if not gas_data or gas_data.created_at < five_seconds_ago or not temp_data or temp_data.created_at < five_seconds_ago:
        gas_data, temp_data = generate_dummy_sensor_data()

    result = {}
    if gas_data:
        result['gas'] = {
            'id': gas_data.id,
            'sensor_type': gas_data.sensor_type,
            'value': gas_data.value,
            'status': gas_data.status,
            'created_at': gas_data.created_at.isoformat()
        }
    if temp_data:
        result['temperature'] = {
            'id': temp_data.id,
            'sensor_type': temp_data.sensor_type,
            'value': temp_data.value,
            'status': temp_data.status,
            'created_at': temp_data.created_at.isoformat()
        }

    response = JsonResponse(result)
    return add_cors_headers(response)

def sensor_stats(request):
    stats = []
    
    for sensor_type in ['gas', 'temperature']:
        data = SensorData.objects.filter(sensor_type=sensor_type).aggregate(
            avg=Avg('value'),
            min=Min('value'),
            max=Max('value'),
            count=Count('id')
        )
        
        if data['count'] > 0:
            stats.append({
                'sensor_type': sensor_type,
                'avg': round(data['avg'], 2) if data['avg'] else 0,
                'min': data['min'] or 0,
                'max': data['max'] or 0,
                'count': data['count']
            })
    
    response = JsonResponse(stats, safe=False)
    return add_cors_headers(response)

@csrf_exempt
def update_threshold(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sensor_type = data['sensor_type']
            threshold, created = Threshold.objects.get_or_create(sensor_type=sensor_type)
            
            threshold.warning_min = data.get('warning_min', threshold.warning_min)
            threshold.warning_max = data.get('warning_max', threshold.warning_max)
            threshold.danger_min = data.get('danger_min', threshold.danger_min)
            threshold.danger_max = data.get('danger_max', threshold.danger_max)
            threshold.save()
            
            response = JsonResponse({
                'sensor_type': threshold.sensor_type,
                'warning_min': threshold.warning_min,
                'warning_max': threshold.warning_max,
                'danger_min': threshold.danger_min,
                'danger_max': threshold.danger_max
            })
            return add_cors_headers(response)
        except Exception as e:
            response = JsonResponse({'error': str(e)}, status=400)
            return add_cors_headers(response)
    
    response = JsonResponse({'error': 'Method not allowed'}, status=405)
    return add_cors_headers(response)

def alerts(request):
    recent_time = timezone.now() - timedelta(hours=24)
    alert_data = SensorData.objects.filter(
        created_at__gte=recent_time,
        status__in=['warning', 'danger']
    ).order_by('-created_at')[:10]
    
    alerts = []
    for data in alert_data:
        message = f"{data.sensor_type.title()} level {data.value} is {data.status}!"
        alerts.append({
            'sensor_type': data.sensor_type,
            'value': data.value,
            'status': data.status,
            'message': message,
            'created_at': data.created_at.isoformat()
        })
    
    response = JsonResponse(alerts, safe=False)
    return add_cors_headers(response)