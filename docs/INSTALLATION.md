# Installation Guide

## Prerequisites

### Hardware Requirements
- **Microcontroller**: Raspberry Pi 4 (4GB RAM minimum) or Arduino Mega 2560
- **Water Quality Sensors**:
  - pH Sensor (Analog output, 0-14 range)
  - Turbidity Sensor (Analog output, 0-100 NTU)
  - TDS Sensor (Analog output, 0-1000 ppm)
  - Temperature Sensor (DS18B20 or analog thermistor)
  - Flow Rate Sensor (Pulse output)
- **Actuators**:
  - 12V DC Pump Motor with relay
  - Solenoid Filter Valve
  - Optional: Chlorine Dosing Pump
- **Power Supply**:
  - Solar Panel (100W recommended)
  - Li-ion Battery Pack (12V, 20Ah)
  - Charge Controller
- **Additional**:
  - ADC Converter (ADS1115 or similar)
  - Relay Module (8-channel)
  - WiFi/GSM Modem
  - Storage: microSD card (32GB)

### Software Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Git
- Internet connection

---

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/varshinir0306/smart-water-purification-system.git
cd smart-water-purification-system
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

If you're on a Raspberry Pi, you might need to install some system packages first:

```bash
sudo apt-get update
sudo apt-get install python3-dev python3-pip
sudo apt-get install libffi-dev libssl-dev
```

### 3. Configure System Settings

Edit `software/config.py` and update:

```python
# WiFi Configuration
WIFI_SSID = "Your WiFi Name"
WIFI_PASSWORD = "Your WiFi Password"

# Firebase Configuration (if using cloud)
FIREBASE_PROJECT_ID = "your-project-id"
FIREBASE_API_KEY = "your-api-key"

# Email Alerts (optional)
EMAIL_SENDER = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"
```

### 4. Set Up Hardware

#### 4a. Connect Sensors to Raspberry Pi

**pH Sensor** → GPIO 34 (ADC)
**Turbidity Sensor** → GPIO 35 (ADC)
**TDS Sensor** → GPIO 32 (ADC)
**Temperature Sensor** → GPIO 33 (ADC)
**Flow Sensor** → GPIO 2 (Digital)

#### 4b. Connect Actuators

**Pump Relay** → GPIO 5
**Filter Valve** → GPIO 12
**Chlorination Pump** → GPIO 13

### 5. Initialize Database

```bash
python software/data_processing.py
```

This will create the SQLite database automatically.

### 6. Test Sensors

```bash
python software/sensors.py
```

You should see sensor readings in the output.

### 7. Test Purification System

```bash
python software/purification.py
```

This tests pump and valve controls.

### 8. Run the Main Application

```bash
python software/main.py
```

The dashboard will be available at: **http://localhost:5000**

---

## Simulation Mode

For testing without real sensors, set in `config.py`:

```python
SIMULATION_MODE = True
```

This generates realistic test data for development.

---

## Troubleshooting

### Issue: GPIO Permission Denied
**Solution:**
```bash
sudo usermod -a -G gpio $(whoami)
```

### Issue: ImportError: No module named 'RPi.GPIO'
**Solution:**
```bash
sudo pip install RPi.GPIO
```

### Issue: Database is locked
**Solution:**
```bash
rm data/water_quality.db
python software/data_processing.py
```

### Issue: WiFi connection fails
**Check:**
1. WiFi credentials in config.py
2. Network is accessible
3. WiFi module is detected: `lsusb`

---

## Next Steps

1. Read [USER_GUIDE.md](USER_GUIDE.md) for daily operation
2. Review [API_REFERENCE.md](API_REFERENCE.md) for advanced features
3. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

---

**Need Help?** Create a GitHub issue or check the documentation.
