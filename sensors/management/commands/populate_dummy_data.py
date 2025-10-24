from django.core.management.base import BaseCommand
from sensors.models import SensorData, Threshold
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate database with dummy sensor data for monitoring'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Populating dummy data...')

        # Create thresholds if they don't exist
        gas_threshold, created = Threshold.objects.get_or_create(
            sensor_type='gas',
            defaults={
                'warning_min': 0,
                'warning_max': 200,
                'danger_min': 0,
                'danger_max': 400
            }
        )
        if created:
            self.stdout.write('✅ Created gas threshold')

        temp_threshold, created = Threshold.objects.get_or_create(
            sensor_type='temperature',
            defaults={
                'warning_min': 0,
                'warning_max': 35,
                'danger_min': 0,
                'danger_max': 50
            }
        )
        if created:
            self.stdout.write('✅ Created temperature threshold')

        # Generate dummy sensor data
        self.stdout.write('📊 Generating dummy sensor data...')

        # Create 20 gas sensor readings
        for i in range(20):
            value = random.uniform(50, 500)  # Gas in ppm
            if value > 400:
                status = 'danger'
            elif value > 200:
                status = 'warning'
            else:
                status = 'normal'

            # Create data with timestamps spread over the last hour
            created_at = datetime.now() - timedelta(minutes=random.randint(0, 60))

            SensorData.objects.create(
                sensor_type='gas',
                value=round(value, 2),
                status=status,
                created_at=created_at
            )

        # Create 20 temperature sensor readings
        for i in range(20):
            value = random.uniform(15, 45)  # Temperature in °C
            if value > 35:
                status = 'warning'
            else:
                status = 'normal'

            # Create data with timestamps spread over the last hour
            created_at = datetime.now() - timedelta(minutes=random.randint(0, 60))

            SensorData.objects.create(
                sensor_type='temperature',
                value=round(value, 2),
                status=status,
                created_at=created_at
            )

        self.stdout.write('✅ Dummy data populated successfully!')
        self.stdout.write(f'📈 Created {SensorData.objects.count()} sensor readings')
        self.stdout.write(f'⚙️  Thresholds configured for gas and temperature')
