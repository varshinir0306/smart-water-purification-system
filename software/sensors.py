# Sensor Data Collection Module
# Handles reading data from water quality sensors

import time
import random
from datetime import datetime
from config import (
    PH_SENSOR_PIN, TURBIDITY_SENSOR_PIN, TDS_SENSOR_PIN, TEMP_SENSOR_PIN,
    PH_ALERT_MIN, PH_ALERT_MAX, TURBIDITY_ALERT_THRESHOLD, TDS_ALERT_THRESHOLD,
    TEMP_ALERT_MIN, TEMP_ALERT_MAX, FLOW_ALERT_MIN, FLOW_ALERT_MAX,
    PH_CALIBRATION_OFFSET, TURBIDITY_CALIBRATION_OFFSET,
    TDS_CALIBRATION_OFFSET, TEMP_CALIBRATION_OFFSET,
    SIMULATION_MODE, SIMULATION_VARIATION, TEST_SEED
)

if SIMULATION_MODE:
    random.seed(TEST_SEED)


class SensorReading:
    """Data class for sensor readings"""
    def __init__(self, ph, turbidity, tds, temperature, flow_rate, timestamp=None):
        self.ph = ph
        self.turbidity = turbidity
        self.tds = tds
        self.temperature = temperature
        self.flow_rate = flow_rate
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self):
        return {
            'ph': round(self.ph, 2),
            'turbidity': round(self.turbidity, 2),
            'tds': round(self.tds, 2),
            'temperature': round(self.temperature, 2),
            'flow_rate': round(self.flow_rate, 2),
            'timestamp': self.timestamp.isoformat()
        }


class WaterQualitySensor:
    """Main sensor class for reading water quality parameters"""
    
    def __init__(self, simulation_mode=SIMULATION_MODE):
        self.simulation_mode = simulation_mode
        self.last_reading = None
        
        # Initialize ADC pins (if not in simulation mode)
        if not self.simulation_mode:
            self._init_hardware()
    
    def _init_hardware(self):
        """Initialize hardware connections"""
        try:
            # Import GPIO library for Raspberry Pi
            import board
            import busio
            # Initialize I2C/ADC connections here
            print("[INFO] Hardware initialized successfully")
        except ImportError:
            print("[WARNING] Hardware initialization libraries not available")
    
    def _simulate_sensor_data(self):
        """Generate simulated sensor data with realistic variations"""
        variation = SIMULATION_VARIATION / 100.0
        
        # Base values (approximate normal readings)
        base_ph = 7.0
        base_turbidity = 2.5
        base_tds = 250
        base_temp = 25
        base_flow = 3.5
        
        # Add random variation
        ph = base_ph + random.uniform(-variation * base_ph, variation * base_ph)
        turbidity = base_turbidity + random.uniform(-variation * base_turbidity, variation * base_turbidity)
        tds = base_tds + random.uniform(-variation * base_tds, variation * base_tds)
        temp = base_temp + random.uniform(-variation * base_temp, variation * base_temp)
        flow = base_flow + random.uniform(-variation * base_flow, variation * base_flow)
        
        # Clamp values to valid ranges
        ph = max(0, min(14, ph))
        turbidity = max(0, min(100, turbidity))
        tds = max(0, min(1000, tds))
        temp = max(-10, min(60, temp))
        flow = max(0, min(15, flow))
        
        return ph, turbidity, tds, temp, flow
    
    def _read_adc(self, pin):
        """Read from ADC pin (not implemented - requires hardware library)"""
        # Placeholder for actual ADC reading
        return 0.0
    
    def read_ph(self):
        """Read pH sensor value (0-14)"""
        if self.simulation_mode:
            _, _, _, _, _ = self._simulate_sensor_data()
            return 7.0 + random.uniform(-0.5, 0.5)
        else:
            # Implement actual reading from pin PH_SENSOR_PIN
            raw_value = self._read_adc(PH_SENSOR_PIN)
            # Convert to pH (example: 0-4095 ADC to 0-14 pH)
            ph = (raw_value / 4095.0) * 14.0
            return ph + PH_CALIBRATION_OFFSET
    
    def read_turbidity(self):
        """Read turbidity sensor value (NTU - Nephelometric Turbidity Units)"""
        if self.simulation_mode:
            _, turbidity, _, _, _ = self._simulate_sensor_data()
            return turbidity
        else:
            raw_value = self._read_adc(TURBIDITY_SENSOR_PIN)
            turbidity = (raw_value / 4095.0) * 100.0
            return turbidity + TURBIDITY_CALIBRATION_OFFSET
    
    def read_tds(self):
        """Read TDS sensor value (ppm - parts per million)"""
        if self.simulation_mode:
            _, _, tds, _, _ = self._simulate_sensor_data()
            return tds
        else:
            raw_value = self._read_adc(TDS_SENSOR_PIN)
            tds = (raw_value / 4095.0) * 1000.0
            return tds + TDS_CALIBRATION_OFFSET
    
    def read_temperature(self):
        """Read temperature sensor value (Celsius)"""
        if self.simulation_mode:
            _, _, _, temp, _ = self._simulate_sensor_data()
            return temp
        else:
            raw_value = self._read_adc(TEMP_SENSOR_PIN)
            # DS18B20 or similar temperature sensor
            temp = (raw_value / 4095.0) * 60.0 - 10.0  # -10 to +50°C range
            return temp + TEMP_CALIBRATION_OFFSET
    
    def read_flow_rate(self):
        """Read flow rate sensor value (L/min)"""
        if self.simulation_mode:
            _, _, _, _, flow = self._simulate_sensor_data()
            return flow
        else:
            # Count pulses from flow sensor (requires interrupt handler)
            # Placeholder - implement pulse counting logic
            return 0.0
    
    def get_all_readings(self):
        """Get all sensor readings in one call"""
        ph = self.read_ph()
        turbidity = self.read_turbidity()
        tds = self.read_tds()
        temperature = self.read_temperature()
        flow_rate = self.read_flow_rate()
        
        reading = SensorReading(ph, turbidity, tds, temperature, flow_rate)
        self.last_reading = reading
        
        return reading
    
    def check_sensor_health(self):
        """Check if all sensors are functioning properly"""
        health_status = {
            'ph_sensor': 'OK',
            'turbidity_sensor': 'OK',
            'tds_sensor': 'OK',
            'temperature_sensor': 'OK',
            'flow_sensor': 'OK',
            'overall': 'HEALTHY'
        }
        
        try:
            reading = self.get_all_readings()
            
            # Check if values are within expected ranges
            if reading.ph < 0 or reading.ph > 14:
                health_status['ph_sensor'] = 'ERROR'
            if reading.turbidity < 0:
                health_status['turbidity_sensor'] = 'ERROR'
            if reading.tds < 0:
                health_status['tds_sensor'] = 'ERROR'
            if reading.temperature < -10 or reading.temperature > 60:
                health_status['temperature_sensor'] = 'ERROR'
            if reading.flow_rate < 0:
                health_status['flow_sensor'] = 'ERROR'
            
            # Check overall status
            if any(v == 'ERROR' for v in list(health_status.values())[:-1]):
                health_status['overall'] = 'DEGRADED'
        
        except Exception as e:
            print(f"[ERROR] Sensor health check failed: {e}")
            health_status['overall'] = 'FAILED'
        
        return health_status


def continuous_sensor_monitoring(sensor, interval=10):
    """Continuously monitor sensors at specified interval"""
    print(f"[INFO] Starting continuous sensor monitoring (interval: {interval}s)")
    
    try:
        while True:
            reading = sensor.get_all_readings()
            print(f"[SENSOR] pH: {reading.ph:.2f} | Turbidity: {reading.turbidity:.2f} NTU | "
                  f"TDS: {reading.tds:.2f} ppm | Temp: {reading.temperature:.2f}°C | "
                  f"Flow: {reading.flow_rate:.2f} L/min")
            
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\n[INFO] Sensor monitoring stopped")


if __name__ == "__main__":
    # Test the sensor module
    sensor = WaterQualitySensor()
    
    print("=" * 60)
    print("Water Quality Sensor Test")
    print("=" * 60)
    
    # Get one reading
    reading = sensor.get_all_readings()
    print("\nCurrent Readings:")
    print(reading.to_dict())
    
    # Check sensor health
    print("\nSensor Health Status:")
    health = sensor.check_sensor_health()
    for key, value in health.items():
        print(f"  {key}: {value}")
    
    # Start continuous monitoring
    print("\nStarting continuous monitoring (Press Ctrl+C to stop)...")
    continuous_sensor_monitoring(sensor, interval=5)
