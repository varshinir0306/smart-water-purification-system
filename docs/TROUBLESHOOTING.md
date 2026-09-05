# Troubleshooting Guide

## Common Issues & Solutions

### 1. System Won't Start

**Error**: `No module named 'RPi.GPIO'`

**Solution**:
```bash
sudo pip install RPi.GPIO
```

**Error**: `Permission denied` when accessing GPIO

**Solution**:
```bash
sudo usermod -a -G gpio $(whoami)
# Then log out and log back in
```

---

### 2. Sensor Reading Issues

**Problem**: All sensors showing 0 or strange values

**Checklist**:
- [ ] Sensors are physically connected
- [ ] Check wiring (loose connections?)
- [ ] Verify pin numbers in config.py
- [ ] Check if ADC converter is working
- [ ] Test sensor individually

**Test Individual Sensor**:
```bash
python -c "from software.sensors import WaterQualitySensor; 
s = WaterQualitySensor(); 
print(s.read_ph())"
```

**Fix**: Recalibrate sensor using calibration values in config.py

---

### 3. Dashboard Not Loading

**Problem**: Browser shows "Cannot reach server"

**Solution**:
1. Check if Flask app is running:
   ```bash
   ps aux | grep main.py
   ```

2. Start the app:
   ```bash
   python software/main.py
   ```

3. Check firewall:
   ```bash
   sudo ufw allow 5000
   ```

4. Verify correct IP:
   ```bash
   hostname -I
   ```

---

### 4. Database Errors

**Error**: `database is locked`

**Solution**:
```bash
# Close all Python processes
pkill -f python

# Backup data if needed
cp data/water_quality.db data/water_quality.db.bak

# Reinitialize
rm data/water_quality.db
python software/data_processing.py
```

**Error**: `table already exists`

**Solution**: Database already initialized. Safe to ignore.

---

### 5. WiFi Connection Issues

**Problem**: System can't connect to WiFi

**Checklist**:
- [ ] SSID and password are correct in config.py
- [ ] WiFi network is accessible
- [ ] WiFi module is detected: `lsusb`
- [ ] Try reboot: `sudo reboot`

**View WiFi Status**:
```bash
iwconfig
```

**Manual WiFi Connection**:
```bash
sudo nmtui
```

---

### 6. Cloud Sync Not Working

**Problem**: Data not syncing to Firebase

**Checklist**:
- [ ] Internet connection is active
- [ ] Firebase credentials in config.py are correct
- [ ] Firebase project exists and is accessible
- [ ] Check logs: `tail -f logs/system.log`

**Test Cloud Connection**:
```bash
python -c "import firebase_admin; print('Firebase loaded successfully')"
```

---

### 7. Alerts Not Being Sent

**Problem**: No email/SMS received even with critical quality

**For Email**:
- [ ] SMTP server is correct (smtp.gmail.com for Gmail)
- [ ] Using app-specific password (not regular Gmail password)
- [ ] Port 587 is correct
- [ ] EMAIL_ALERTS_ENABLED = True in config.py
- [ ] Recipient emails are valid

**Test Email**:
```bash
python -c "from software.notifications import send_email; 
send_email('test@example.com', 'Test', 'This is a test')"
```

**For SMS**:
- [ ] Twilio account is active and verified
- [ ] Twilio credentials are correct
- [ ] Phone numbers include country code (+1, +91, etc.)
- [ ] Account has sufficient balance
- [ ] SMS_ALERTS_ENABLED = True

---

### 8. Pump Not Activating

**Problem**: Pump doesn't turn on even with poor water quality

**Checklist**:
- [ ] Power supply to pump is connected
- [ ] Relay module is connected to GPIO 5
- [ ] PUMP_AUTO_MODE = True in config.py
- [ ] Quality score is actually < PUMP_ON_THRESHOLD (60)
- [ ] Check relay with multimeter

**Test Pump Manually**:
```bash
python -c "from software.purification import PurificationSystem; 
sys = PurificationSystem(); 
sys.activate_pump()"
```

---

### 9. High CPU Usage

**Problem**: Raspberry Pi getting hot, slow response

**Solution**:
1. Increase sensor sampling interval:
   ```python
   DATA_LOG_INTERVAL = 30  # From 10 to 30 seconds
   ```

2. Reduce cloud sync frequency:
   ```python
   CLOUD_SYNC_INTERVAL = 300  # From 60 to 300 seconds
   ```

3. Limit historical data display:
   ```python
   MAX_LOCAL_RECORDS = 10000  # Reduce if needed
   ```

4. Check running processes:
   ```bash
   top
   ```

---

### 10. Battery Not Charging

**Problem**: Battery level stuck at same percentage

**Checklist**:
- [ ] Solar panel is in sunlight
- [ ] Panel connections are secure
- [ ] Charge controller is receiving power
- [ ] Battery is not completely dead (< 9V)
- [ ] Check voltage: `cat /sys/class/hwmon/hwmon0/in0_input`

**Reset Battery Monitor**:
```bash
# Cycle power: disconnect battery, wait 30s, reconnect
```

---

### 11. Sensor Drifting Over Time

**Problem**: Sensor readings gradually change without real water changes

**Solution**: Sensor calibration needed

**Calibration Steps**:
1. Get known reference solutions
2. Measure with sensor
3. Calculate offset: known_value - sensor_reading
4. Update config.py with offset:
   ```python
   PH_CALIBRATION_OFFSET = 0.2  # Example
   ```

---

### 12. System Crashes or Reboots

**Check Logs**:
```bash
journalctl -xe
```

**Common Causes**:
- Insufficient RAM: Check with `free -h`
- Temperature too high: Check with `vcgencmd measure_temp`
- Corrupted storage: Run `fsck`

**Solution**:
```bash
# Restart system
sudo reboot

# Check disk space
df -h

# Clear logs if full
sudo journalctl --vacuum=50M
```

---

## Getting Help

### Enable Debug Mode

```python
# In config.py
DEBUG_MODE = True
LOG_LEVEL = "DEBUG"
```

### View System Logs

```bash
# Real-time logs
tail -f logs/system.log

# Last 100 lines
tail -100 logs/system.log

# Search for errors
grep ERROR logs/system.log
```

### Create Diagnostic Report

```bash
# Collect system info
echo "=== System Info ==="
uname -a
echo "=== Python Version ==="
python --version
echo "=== Installed Packages ==="
pip list
echo "=== Disk Space ==="
df -h
echo "=== Memory ==="
free -h
echo "=== Temperature ==="
vcgencmd measure_temp
```

### Report an Issue

When creating a GitHub issue, include:
1. Error message (full text)
2. Last 50 lines of log file
3. Your hardware configuration
4. Steps to reproduce
5. Diagnostic report (from above)

---

**Still Having Issues?** 

1. Check logs carefully
2. Try restarting the system
3. Verify all connections
4. Create a detailed GitHub issue
5. Contact project maintainers
