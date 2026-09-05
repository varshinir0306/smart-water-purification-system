# User Guide

## Getting Started

Once your system is installed and running, here's how to use it.

### Accessing the Dashboard

1. **Start the Application**:
   ```bash
   python software/main.py
   ```

2. **Open Dashboard**:
   - Local: http://localhost:5000
   - Remote: http://<your-pi-ip>:5000

### Understanding the Dashboard

#### Real-Time Metrics

**pH Level** (6.5 - 8.5 ideal)
- Shows current water acidity/alkalinity
- Red indicator: Out of range
- Green indicator: Normal

**Turbidity** (< 5 NTU ideal)
- Measures water cloudiness
- High values indicate particles/contamination

**TDS** (Total Dissolved Solids, < 500 ppm ideal)
- Amount of dissolved minerals
- Affects water taste and quality

**Temperature** (10 - 40°C ideal)
- Water temperature
- Affects bacterial growth and chemical reactions

**Flow Rate** (0.5 - 10 L/min ideal)
- Current water flow through system
- Low flow: Check for clogs
- High flow: Pressure issue

**Quality Score** (0-100)
- Overall water safety assessment
- **80-100**: Good (Safe to consume)
- **60-79**: Fair (Monitor)
- **40-59**: Poor (Treatment needed)
- **0-39**: Critical (Do not consume)

---

## System Controls

### Automatic Operation

The system can operate automatically based on water quality:

1. **Poor Quality** (Score < 60)
   - ✅ Pump activates automatically
   - ✅ Filtration increases
   - ✅ Possible chlorination

2. **Good Quality** (Score > 80)
   - ✅ Pump may reduce speed
   - ✅ Normal filtration continues
   - ✅ Chlorination stops

### Manual Controls

To manually control the system:

1. **Stop Automatic Mode**:
   Edit `software/config.py`:
   ```python
   PUMP_AUTO_MODE = False
   ```

2. **Manual Pump Control**:
   ```python
   # In Python console
   from software.purification import PurificationSystem
   system = PurificationSystem()
   system.activate_pump()    # Turn on
   system.deactivate_pump()  # Turn off
   ```

3. **Filter Maintenance**:
   The system alerts when filter cleaning is needed (every 1 hour by default).
   ```python
   system.start_filter_cleaning()  # Manual cleaning cycle
   ```

---

## Alerts & Notifications

### Alert Types

1. **CRITICAL** (Red)
   - Quality < 40
   - Immediate action needed
   - Email/SMS sent (if enabled)

2. **WARNING** (Yellow)
   - Quality 40-60
   - Close monitoring required
   - Notification sent

3. **CAUTION** (Blue)
   - Quality 60-80
   - Routine checks recommended

4. **NORMAL** (Green)
   - Quality > 80
   - Continue normal operation

### Receiving Alerts

**Email Alerts**:
1. Enable in `config.py`:
   ```python
   EMAIL_ALERTS_ENABLED = True
   ```
2. Add recipient emails
3. Use Gmail app password (not regular password)

**SMS Alerts**:
1. Set up Twilio account
2. Enable in `config.py`:
   ```python
   SMS_ALERTS_ENABLED = True
   ```
3. Add phone numbers

---

## Viewing Historical Data

### In Dashboard
- Scroll down to "Historical Readings" table
- Shows last 100 readings with timestamps
- Refresh automatically every 10 seconds

### Via API
```bash
curl http://localhost:5000/api/readings?hours=24
```

### Export Data
```bash
# Export to CSV
python -c "from software.data_processing import DataStorage; 
db = DataStorage(); 
readings = db.get_readings_since(24)"
```

---

## Maintenance Tasks

### Daily Checklist
- ✓ Check dashboard for any warnings
- ✓ Verify system is online
- ✓ Look for any red alerts
- ✓ Check water output quality

### Weekly
- ✓ Review water quality trends
- ✓ Check sensor readings for consistency
- ✓ Verify battery level (if solar powered)
- ✓ Look for physical water leaks

### Monthly
- ✓ Clean filters manually if needed
- ✓ Recalibrate sensors (if drift detected)
- ✓ Review system logs
- ✓ Update software (if updates available)
- ✓ Test alert system (manual test)

### Every 6 Months
- ✓ Professional sensor calibration
- ✓ Replace filter cartridges
- ✓ Full system inspection
- ✓ Backup all data

---

## Common Scenarios

### Scenario 1: pH Too Low (Acidic)

**Cause**: Acid contamination or natural acidity

**Actions**:
1. Check water source
2. Add alkaline treatment (calcium carbonate)
3. Monitor pH trend
4. Recalibrate pH sensor if needed

### Scenario 2: High Turbidity

**Cause**: Suspended particles, sediment

**Actions**:
1. Check filter status
2. Increase filtration rate
3. Perform filter cleaning
4. Check water source for pollution

### Scenario 3: High TDS

**Cause**: Dissolved minerals, salt, chemicals

**Actions**:
1. Use reverse osmosis filter
2. Increase water exchange rate
3. Check for contamination source
4. May need different filtration system

### Scenario 4: Temperature Issues

**Cause**: Season changes, ambient temperature

**Actions**:
1. Insulate pipes if too cold
2. Add cooling if too hot
3. Check temperature sensor calibration

### Scenario 5: Low Flow Rate

**Cause**: Clogged filter, system issue

**Actions**:
1. Clean/replace filters immediately
2. Check for leaks
3. Verify pump is running
4. Check valve positions

---

## Power Management (Solar Systems)

### Battery Monitoring
- Dashboard shows current battery level
- Low power mode activates at < 11.5V
- Critical shutdown at < 10.5V

### Extending Battery Life
1. Reduce sampling frequency
2. Disable cloud sync during off-peak
3. Use sleep mode for low usage periods
4. Keep battery temperature optimal

---

## Getting Help

1. **Check Logs**:
   ```bash
   tail -f logs/system.log
   ```

2. **Sensor Diagnostics**:
   Visit http://localhost:5000/api/diagnostics

3. **System Status**:
   Visit http://localhost:5000/api/status

4. **Report Issue**:
   Create GitHub issue with:
   - Error message
   - System logs
   - Recent readings
   - Hardware configuration

---

**Questions?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or create an issue on GitHub.
