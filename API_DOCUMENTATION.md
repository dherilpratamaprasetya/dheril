# 🚀 IoT Dashboard API Documentation

## Base URL
```
http://127.0.0.1:8000/api
```

## 📊 Endpoints

### 1. Sensor Data Management

#### GET /sensors/
Get all sensor data (latest 20 records)

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "sensor_type": "gas",
      "value": 250.5,
      "status": "warning",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### POST /sensors/
Add new sensor data

**Request Body:**
```json
{
  "sensor_type": "gas",
  "value": 250.5,
  "status": "warning"
}
```

### 2. Latest Data

#### GET /sensors/latest/
Get latest sensor data for gas and temperature

**Response:**
```json
{
  "gas": {
    "id": 1,
    "sensor_type": "gas",
    "value": 320.0,
    "status": "danger",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "temperature": {
    "id": 2,
    "sensor_type": "temperature",
    "value": 27.5,
    "status": "normal",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

### 3. Statistics

#### GET /sensors/stats/
Get sensor statistics (avg, min, max, count)

**Response:**
```json
[
  {
    "sensor_type": "gas",
    "avg": 275.50,
    "min": 100.0,
    "max": 450.0,
    "count": 10
  },
  {
    "sensor_type": "temperature",
    "avg": 28.75,
    "min": 20.0,
    "max": 35.0,
    "count": 10
  }
]
```

### 4. Threshold Management

#### POST /settings/threshold/
Update sensor thresholds

**Request Body:**
```json
{
  "sensor_type": "gas",
  "warning_min": 0,
  "warning_max": 300,
  "danger_min": 300,
  "danger_max": 1000
}
```

### 5. Alerts

#### GET /alerts/
Get recent alerts (last 24 hours)

**Response:**
```json
[
  {
    "sensor_type": "gas",
    "value": 450.0,
    "status": "danger",
    "message": "Gas level 450.0 is danger!",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

## 🧪 Testing with cURL

### Add Gas Data
```bash
curl -X POST http://127.0.0.1:8000/api/sensors/ \
  -H "Content-Type: application/json" \
  -d '{"sensor_type": "gas", "value": 320.5, "status": "danger"}'
```

### Add Temperature Data
```bash
curl -X POST http://127.0.0.1:8000/api/sensors/ \
  -H "Content-Type: application/json" \
  -d '{"sensor_type": "temperature", "value": 28.5, "status": "normal"}'
```

### Get Latest Data
```bash
curl http://127.0.0.1:8000/api/sensors/latest/
```

### Get Statistics
```bash
curl http://127.0.0.1:8000/api/sensors/stats/
```

### Update Threshold
```bash
curl -X POST http://127.0.0.1:8000/api/settings/threshold/ \
  -H "Content-Type: application/json" \
  -d '{"sensor_type": "gas", "warning_max": 300, "danger_min": 300}'
```

## 🔄 Status Codes

- **200**: Success
- **400**: Bad Request (invalid data)
- **405**: Method Not Allowed
- **500**: Server Error

## 📱 Frontend Integration

### JavaScript/React Example
```javascript
// Get latest sensor data
const getLatestData = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/sensors/latest/');
    const data = await response.json();
    console.log('Latest data:', data);
  } catch (error) {
    console.error('Error:', error);
  }
};

// Real-time polling (every 5 seconds)
setInterval(getLatestData, 5000);
```

## 🚀 Quick Start

1. **Start Django Server:**
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Start IoT Simulation:**
   ```bash
   cd backend
   python sensors/simulate.py
   ```

3. **Test API:**
   ```bash
   python test_api.py
   ```

4. **Access Admin Panel:**
   ```
   http://127.0.0.1:8000/admin/
   ```