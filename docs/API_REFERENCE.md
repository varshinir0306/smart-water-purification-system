# API Reference

## Base URL

```
http://localhost:5000
```

## Endpoints

### Dashboard & UI

#### GET /
**Description**: Returns the main dashboard HTML

**Response**: HTML page

**Example**:
```bash
curl http://localhost:5000/
```

---

### Real-Time Data

#### GET /api/readings/latest
**Description**: Get the latest sensor reading

**Response**:
```json
{
  "ph": 7.2,
  "turbidity": 2.5,
  "tds": 300,
  "temperature": 25.5,
  "flow_rate": 3.5,
  "quality_score": 85.3,
  "status": "Good",
  "timestamp": "2024-01-15T10:30:45.123Z"
}
```

**Example**:
```bash
curl http://localhost:5000/api/readings/latest
```

---

#### GET /api/readings
**Description**: Get readings with optional filters

**Query Parameters**:
- `limit` (int, default: 100) - Number of readings to return
- `hours` (int, default: 24) - Get readings from last N hours
- `status` (string) - Filter by status: 'Good', 'Fair', 'Poor', 'Critical'

**Response**: Array of readings

**Example**:
```bash
# Last 50 readings
curl http://localhost:5000/api/readings?limit=50

# Last 7 days of data
curl http://localhost:5000/api/readings?hours=168

# Only good quality readings
curl http://localhost:5000/api/readings?status=Good
```

---

### Statistics

#### GET /api/statistics
**Description**: Get statistical summary of readings

**Query Parameters**:
- `hours` (int, default: 24) - Time period for statistics

**Response**:
```json
{
  "avg_ph": 7.15,
  "min_ph": 6.8,
  "max_ph": 7.6,
  "avg_turbidity": 2.3,
  "avg_tds": 285,
  "avg_temperature": 24.8,
  "avg_quality_score": 83.5,
  "reading_count": 1440,
  "period_hours": 24
}
```

**Example**:
```bash
# Last 24 hours statistics
curl http://localhost:5000/api/statistics?hours=24

# Last 7 days statistics
curl http://localhost:5000/api/statistics?hours=168
```

---

### System Status

#### GET /api/status
**Description**: Get current system status

**Response**:
```json
{
  "system_online": true,
  "pump_active": true,
  "filter_cleaning_needed": false,
  "chlorination_active": false,
  "last_reading_time": "2024-01-15T10:35:12.456Z",
  "uptime_seconds": 86400,
  "sensor_health": {
    "ph_sensor": "OK",
    "turbidity_sensor": "OK",
    "tds_sensor": "OK",
    "temperature_sensor": "OK",
    "flow_sensor": "OK",
    "overall": "HEALTHY"
  },
  "battery_level": 85,
  "solar_charging": true
}
```

**Example**:
```bash
curl http://localhost:5000/api/status
```

---

### Alerts

#### GET /api/alerts
**Description**: Get all active alerts

**Query Parameters**:
- `severity` (string) - Filter by severity: 'CRITICAL', 'WARNING', 'CAUTION'
- `unread` (boolean) - Show only unread alerts

**Response**: Array of alerts

**Example**:
```bash
# All critical alerts
curl http://localhost:5000/api/alerts?severity=CRITICAL

# Unread alerts only
curl http://localhost:5000/api/alerts?unread=true
```

---

#### POST /api/alerts/mark-read
**Description**: Mark alerts as read

**Request Body**:
```json
{
  "alert_ids": [1, 2, 3]
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/alerts/mark-read \
  -H "Content-Type: application/json" \
  -d '{"alert_ids": [1, 2]}'
```

---

### System Control

#### POST /api/pump/on
**Description**: Manually turn on the pump

**Response**:
```json
{
  "success": true,
  "message": "Pump activated",
  "timestamp": "2024-01-15T10:36:00.000Z"
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/pump/on
```

---

#### POST /api/pump/off
**Description**: Manually turn off the pump

**Example**:
```bash
curl -X POST http://localhost:5000/api/pump/off
```

---

#### POST /api/pump/auto
**Description**: Enable automatic pump control

**Request Body** (optional):
```json
{
  "on_threshold": 60,
  "off_threshold": 85
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/pump/auto \
  -H "Content-Type: application/json" \
  -d '{"on_threshold": 60, "off_threshold": 85}'
```

---

#### POST /api/filter/clean
**Description**: Start manual filter cleaning cycle

**Response**:
```json
{
  "success": true,
  "message": "Filter cleaning started",
  "duration_seconds": 300
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/filter/clean
```

---

#### POST /api/chlorination/on
**Description**: Enable chlorination system

**Example**:
```bash
curl -X POST http://localhost:5000/api/chlorination/on
```

---

#### POST /api/chlorination/off
**Description**: Disable chlorination system

**Example**:
```bash
curl -X POST http://localhost:5000/api/chlorination/off
```

---

### Configuration

#### GET /api/config
**Description**: Get current system configuration

**Response**: JSON object with all configuration parameters

**Example**:
```bash
curl http://localhost:5000/api/config
```

---

#### POST /api/config
**Description**: Update configuration parameters

**Request Body**:
```json
{
  "PUMP_ON_THRESHOLD": 55,
  "PUMP_OFF_THRESHOLD": 90,
  "FILTER_CLEANING_INTERVAL": 7200
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/config \
  -H "Content-Type: application/json" \
  -d '{"PUMP_ON_THRESHOLD": 55}'
```

---

### Diagnostics

#### GET /api/diagnostics
**Description**: Get detailed system diagnostics

**Response**:
```json
{
  "system_info": {
    "platform": "linux",
    "python_version": "3.9.2",
    "uptime": 86400
  },
  "sensor_diagnostics": {
    "last_reading": "2024-01-15T10:35:12Z",
    "reading_interval": 10,
    "failed_readings": 0
  },
  "database": {
    "total_records": 8640,
    "database_size_mb": 5.2
  },
  "network": {
    "wifi_connected": true,
    "signal_strength": -45,
    "cloud_synced": true
  }
}
```

**Example**:
```bash
curl http://localhost:5000/api/diagnostics
```

---

### Export Data

#### GET /api/export/csv
**Description**: Export readings as CSV

**Query Parameters**:
- `hours` (int, default: 24) - Time period to export
- `include_stats` (boolean, default: false) - Include statistics summary

**Response**: CSV file download

**Example**:
```bash
# Export last 24 hours
curl http://localhost:5000/api/export/csv?hours=24 > readings.csv

# Export with statistics
curl http://localhost:5000/api/export/csv?hours=168&include_stats=true > readings.csv
```

---

#### GET /api/export/json
**Description**: Export readings as JSON

**Example**:
```bash
curl http://localhost:5000/api/export/json?hours=24 > readings.json
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid parameter",
  "message": "Parameter 'hours' must be a positive integer"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found",
  "message": "Alert with ID 999 not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Server error",
  "message": "Database connection failed"
}
```

---

## Rate Limiting

API requests are limited to:
- **100 requests per minute** for normal endpoints
- **10 requests per minute** for control endpoints (pump, filter, etc.)

Exceeding limits returns:
```json
{
  "error": "Rate limit exceeded",
  "retry_after_seconds": 30
}
```

---

## Authentication

Current version has no authentication. For production, implement:

```python
# Add to requests
headers = {
  'Authorization': 'Bearer YOUR_API_TOKEN',
  'Content-Type': 'application/json'
}
```

---

## Webhooks (Future)

Plan to support webhooks for:
- Critical alerts
- Data updates
- System state changes

---

## SDK/Libraries

**Python Client**:
```python
from smart_water import Client
client = Client('http://localhost:5000')
readings = client.get_latest_reading()
print(readings.quality_score)
```

---

## Changelog

**v1.0.0** (Current)
- Initial API release
- Core endpoints implemented
- CSV/JSON export

**v1.1.0** (Planned)
- Webhook support
- Authentication/API keys
- GraphQL endpoint
- Historical data analytics

---

**Questions?** Create an issue or contact project maintainers.
