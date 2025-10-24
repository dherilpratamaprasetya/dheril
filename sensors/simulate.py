import os
import sys
import django
import random
import time
from datetime import datetime

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from sensors.models import SensorData

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

def generate_sensor_data():
    """Generate random sensor data"""
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
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Generated - Gas: {gas_value:.2f}ppm ({gas_status}), Temp: {temp_value:.2f}°C ({temp_status})")
    
    return gas_data, temp_data

def main():
    """Main simulation loop"""
    print("🚀 Starting IoT Sensor Simulation...")
    print("📊 Generating data every 5 seconds...")
    print("⚠️  Press Ctrl+C to stop\n")
    
    try:
        while True:
            generate_sensor_data()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()