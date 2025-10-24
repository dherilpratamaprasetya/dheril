from django.shortcuts import render
from django.http import JsonResponse
import requests

def dashboard(request):
    return render(request, 'frontend/dashboard.html')

def get_sensor_data(request):
    try:
        # Fetch data from API (adjust URL for production)
        base_url = request.build_absolute_uri('/').rstrip('/')
        response = requests.get(f'{base_url}/api/sensors/latest/')
        data = response.json()
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
