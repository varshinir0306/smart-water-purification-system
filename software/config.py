# Configuration file for Smart Water Purification System

# ============================================================================
# SENSOR CALIBRATION & SETTINGS
# ============================================================================

# pH Sensor Configuration
PH_SENSOR_PIN = 34  # ADC pin for pH sensor
PH_MIN = 0
PH_MAX = 14
PH_CALIBRATION_OFFSET = 0.0  # Fine-tune pH readings
PH_ALERT_MIN = 6.5
PH_ALERT_MAX = 8.5

# Turbidity Sensor Configuration
TURBIDITY_SENSOR_PIN = 35  # ADC pin for turbidity sensor
TURBIDITY_MIN = 0
TURBIDITY_MAX = 100  # in NTU (Nephelometric Turbidity Units)
TURBIDITY_CALIBRATION_OFFSET = 0.0
TURBIDITY_ALERT_THRESHOLD = 5  # Alert if > 5 NTU

# TDS Sensor Configuration (Total Dissolved Solids)
TDS_SENSOR_PIN = 32  # ADC pin for TDS sensor
TDS_MIN = 0
TDS_MAX = 1000  # in ppm (parts per million)
TDS_CALIBRATION_OFFSET = 0.0
TDS_ALERT_THRESHOLD = 500  # Alert if > 500 ppm

# Temperature Sensor Configuration
TEMP_SENSOR_PIN = 33  # ADC pin for temperature sensor
TEMP_MIN = 0
TEMP_MAX = 60  # in Celsius
TEMP_CALIBRATION_OFFSET = 0.0
TEMP_ALERT_MIN = 10  # Alert if < 10°C
TEMP_ALERT_MAX = 40  # Alert if > 40°C

# Flow Rate Sensor Configuration
FLOW_SENSOR_PIN = 2  # GPIO pin for flow sensor (pulse counter)
FLOW_CALIBRATION_FACTOR = 1.0  # pulses per liter
FLOW_ALERT_MIN = 0.5  # Alert if < 0.5 L/min
FLOW_ALERT_MAX = 10.0  # Alert if > 10 L/min

# ============================================================================
# PURIFICATION SYSTEM CONTROL
# ============================================================================

# Pump Control
PUMP_MOTOR_PIN = 5  # GPIO pin for pump relay
PUMP_AUTO_MODE = True  # Enable automatic pump control
PUMP_ON_THRESHOLD = 60  # Activate pump if quality score < 60
PUMP_OFF_THRESHOLD = 85  # Deactivate pump if quality score > 85

# Filter Valve Control
FILTER_VALVE_PIN = 12  # GPIO pin for filter valve
FILTER_CLEANING_INTERVAL = 3600  # seconds (1 hour)
FILTER_CLEANING_DURATION = 300  # seconds (5 minutes)

# Chlorination System (Optional)
CHLORINATION_ENABLED = False
CHLORINATION_PUMP_PIN = 13
CHLORINATION_DOSE_PPM = 0.5  # mg/L

# ============================================================================
# DATA LOGGING & STORAGE
# ============================================================================

# Local Database
LOCAL_DB_PATH = "data/water_quality.db"
DATA_LOG_INTERVAL = 10  # seconds (log data every 10 seconds)
MAX_LOCAL_RECORDS = 100000  # Maximum records before cleanup

# CSV Logging
CSV_LOG_ENABLED = True
CSV_LOG_PATH = "data/readings.csv"

# ============================================================================
# CLOUD INTEGRATION (Firebase / AWS)
# ============================================================================

# Firebase Configuration
FIREBASE_ENABLED = True
FIREBASE_PROJECT_ID = "your-firebase-project-id"
FIREBASE_API_KEY = "your-firebase-api-key"
FIREBASE_DATABASE_URL = "https://your-project.firebaseio.com"
FIREBASE_STORAGE_BUCKET = "your-project.appspot.com"

# Cloud Sync Interval
CLOUD_SYNC_INTERVAL = 60  # seconds (sync to cloud every minute)
CLOUD_BATCH_SIZE = 50  # Push 50 records at a time

# ============================================================================
# NETWORK & CONNECTIVITY
# ============================================================================

# WiFi Configuration
WIFI_SSID = "YourWiFiName"
WIFI_PASSWORD = "YourWiFiPassword"
WIFI_TIMEOUT = 10  # seconds

# Fallback GSM/Mobile Network (Optional)
GSM_ENABLED = False
GSM_APN = "your-gsm-apn"
GSM_USERNAME = "username"
GSM_PASSWORD = "password"

# Server Configuration
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000
DEBUG_MODE = True

# ============================================================================
# ALERT & NOTIFICATION SETTINGS
# ============================================================================

# Alert Thresholds
ALERT_ENABLED = True
CRITICAL_ALERT_THRESHOLD = 40  # Quality score < 40 = Critical
WARNING_ALERT_THRESHOLD = 60  # Quality score < 60 = Warning

# Email Alerts
EMAIL_ALERTS_ENABLED = False
EMAIL_SENDER = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"  # Use Gmail app password
EMAIL_RECIPIENTS = ["admin@example.com", "operator@example.com"]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# SMS Alerts (Twilio)
SMS_ALERTS_ENABLED = False
TWILIO_ACCOUNT_SID = "your-twilio-account-sid"
TWILIO_AUTH_TOKEN = "your-twilio-auth-token"
TWILIO_FROM_NUMBER = "+1234567890"
SMS_RECIPIENTS = ["+91XXXXXXXXXX", "+91YYYYYYYYYY"]

# Push Notifications
PUSH_NOTIFICATIONS_ENABLED = False
FCM_API_KEY = "your-firebase-cloud-messaging-key"

# ============================================================================
# POWER MANAGEMENT
# ============================================================================

# Solar Panel Configuration
SOLAR_PANEL_ENABLED = True
SOLAR_VOLTAGE_PIN = 36  # ADC pin for solar voltage monitoring
SOLAR_MIN_VOLTAGE = 12  # Volts
SOLAR_MAX_VOLTAGE = 18  # Volts

# Battery Configuration
BATTERY_ENABLED = True
BATTERY_VOLTAGE_PIN = 37  # ADC pin for battery voltage
BATTERY_MIN_VOLTAGE = 10.5  # Volts (Critical - enter shutdown mode)
BATTERY_LOW_VOLTAGE = 11.5  # Volts (Warning level)
BATTERY_FULL_VOLTAGE = 14.0  # Volts

# Low Power Mode
LOW_POWER_MODE_ENABLED = True
LOW_POWER_VOLTAGE_THRESHOLD = 11.5  # Activate low power mode
LOW_POWER_SAMPLING_INTERVAL = 60  # seconds (slower sampling)
LOW_POWER_CLOUD_SYNC_INTERVAL = 300  # seconds (5 minutes)

# ============================================================================
# MAINTENANCE & DIAGNOSTICS
# ============================================================================

# System Health Check
HEALTH_CHECK_INTERVAL = 600  # seconds (every 10 minutes)
SENSOR_TIMEOUT = 30  # seconds (sensor considered offline if no reading)

# Sensor Diagnostics
DIAGNOSTICS_ENABLED = True
DIAGNOSTICS_LOG_PATH = "data/diagnostics.log"

# Sensor Recalibration Reminders
RECALIBRATION_INTERVAL = 604800  # seconds (7 days)
RECALIBRATION_ALERT_DAYS = 1  # Days before recalibration is due

# ============================================================================
# WATER QUALITY SCORING ALGORITHM
# ============================================================================

# Quality Score Weights (total should = 100)
PH_WEIGHT = 25
TURBIDITY_WEIGHT = 30
TDS_WEIGHT = 25
TEMP_WEIGHT = 10
FLOW_WEIGHT = 10

# Status Categories
QUALITY_SCORE_GOOD = 80  # Score >= 80 = Good
QUALITY_SCORE_FAIR = 60  # 60 <= Score < 80 = Fair
QUALITY_SCORE_POOR = 40  # 40 <= Score < 60 = Poor
QUALITY_SCORE_CRITICAL = 0  # Score < 40 = Critical

# ============================================================================
# SYSTEM LOGGING
# ============================================================================

# Log Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = "INFO"
LOG_FILE = "logs/system.log"
LOG_MAX_SIZE = 5242880  # 5 MB
LOG_BACKUP_COUNT = 5

# ============================================================================
# TESTING & SIMULATION
# ============================================================================

# Simulation Mode (for testing without real sensors)
SIMULATION_MODE = True
SIMULATION_VARIATION = 5  # Random variation ±5%

# Test Data Seed
TEST_SEED = 42  # For reproducible test data
