# Purification System Control Module
# Handles automatic pump, filter, and treatment controls

import time
from datetime import datetime
from config import (
    PUMP_MOTOR_PIN, PUMP_AUTO_MODE, PUMP_ON_THRESHOLD, PUMP_OFF_THRESHOLD,
    FILTER_VALVE_PIN, FILTER_CLEANING_INTERVAL, FILTER_CLEANING_DURATION,
    CHLORINATION_ENABLED, CHLORINATION_PUMP_PIN, CHLORINATION_DOSE_PPM
)


class PurificationSystem:
    """Control system for water purification equipment"""
    
    def __init__(self):
        self.pump_active = False
        self.filter_cleaning_needed = False
        self.chlorination_active = CHLORINATION_ENABLED
        self.last_filter_clean_time = datetime.now()
        self.system_uptime = 0
        
        # Initialize GPIO pins if hardware mode
        self._init_hardware()
    
    def _init_hardware(self):
        """Initialize GPIO pins for motor and valve control"""
        try:
            # Try to import GPIO library
            # import RPi.GPIO as GPIO
            # GPIO.setmode(GPIO.BCM)
            # GPIO.setup(PUMP_MOTOR_PIN, GPIO.OUT)
            # GPIO.setup(FILTER_VALVE_PIN, GPIO.OUT)
            # GPIO.output(PUMP_MOTOR_PIN, GPIO.LOW)  # Start with pump OFF
            # GPIO.output(FILTER_VALVE_PIN, GPIO.LOW)  # Filter valve OFF
            print("[INFO] Purification system hardware initialized")
        except Exception as e:
            print(f"[WARNING] Could not initialize GPIO: {e}")
    
    def activate_pump(self):
        """Turn on the water purification pump"""
        if not self.pump_active:
            print("[CONTROL] Activating purification pump...")
            # GPIO.output(PUMP_MOTOR_PIN, GPIO.HIGH)
            self.pump_active = True
            return True
        return False
    
    def deactivate_pump(self):
        """Turn off the water purification pump"""
        if self.pump_active:
            print("[CONTROL] Deactivating purification pump...")
            # GPIO.output(PUMP_MOTOR_PIN, GPIO.LOW)
            self.pump_active = False
            return True
        return False
    
    def open_filter_valve(self):
        """Open filter valve for water flow"""
        print("[CONTROL] Opening filter valve...")
        # GPIO.output(FILTER_VALVE_PIN, GPIO.HIGH)
        return True
    
    def close_filter_valve(self):
        """Close filter valve for maintenance"""
        print("[CONTROL] Closing filter valve...")
        # GPIO.output(FILTER_VALVE_PIN, GPIO.LOW)
        return True
    
    def start_filter_cleaning(self):
        """Initiate automatic filter cleaning cycle"""
        print("[MAINTENANCE] Starting filter cleaning cycle...")
        self.deactivate_pump()
        time.sleep(2)  # Wait for pressure to drop
        self.close_filter_valve()
        
        # Run backflush cycle
        print(f"[MAINTENANCE] Running backflush for {FILTER_CLEANING_DURATION} seconds...")
        time.sleep(FILTER_CLEANING_DURATION)
        
        print("[MAINTENANCE] Filter cleaning complete")
        self.open_filter_valve()
        self.activate_pump()
        self.last_filter_clean_time = datetime.now()
        self.filter_cleaning_needed = False
    
    def enable_chlorination(self):
        """Enable chlorine dosing system"""
        if CHLORINATION_ENABLED:
            print(f"[CONTROL] Enabling chlorination ({CHLORINATION_DOSE_PPM} ppm)...")
            # GPIO.output(CHLORINATION_PUMP_PIN, GPIO.HIGH)
            self.chlorination_active = True
            return True
        return False
    
    def disable_chlorination(self):
        """Disable chlorine dosing system"""
        if self.chlorination_active:
            print("[CONTROL] Disabling chlorination...")
            # GPIO.output(CHLORINATION_PUMP_PIN, GPIO.LOW)
            self.chlorination_active = False
            return True
        return False
    
    def check_filter_maintenance(self):
        """Check if filter cleaning is needed"""
        time_since_clean = (datetime.now() - self.last_filter_clean_time).total_seconds()
        
        if time_since_clean >= FILTER_CLEANING_INTERVAL:
            self.filter_cleaning_needed = True
            return True
        return False
    
    def auto_control(self, quality_score):
        """Automatically control purification system based on water quality score"""
        if not PUMP_AUTO_MODE:
            return
        
        # Activate pump if quality is poor
        if quality_score < PUMP_ON_THRESHOLD:
            if not self.pump_active:
                self.activate_pump()
                if quality_score < 40:  # Critical
                    self.enable_chlorination()
        
        # Deactivate pump if quality improves
        elif quality_score > PUMP_OFF_THRESHOLD:
            if self.pump_active:
                self.deactivate_pump()
                if quality_score > 80:  # Good
                    self.disable_chlorination()
        
        # Check if filter cleaning is needed
        if self.check_filter_maintenance():
            print("[ALERT] Filter cleaning is due!")
            # Schedule cleaning (can be done during off-peak hours)
    
    def get_system_status(self):
        """Get current purification system status"""
        return {
            'pump_active': self.pump_active,
            'filter_cleaning_needed': self.filter_cleaning_needed,
            'chlorination_active': self.chlorination_active,
            'last_filter_clean': self.last_filter_clean_time.isoformat(),
            'time_since_clean': (datetime.now() - self.last_filter_clean_time).total_seconds(),
            'auto_mode': PUMP_AUTO_MODE
        }


class ActionRecommender:
    """Recommend actions based on water quality readings"""
    
    @staticmethod
    def get_recommendation(reading, quality_score):
        """
        Get recommended actions based on sensor readings and quality score
        Returns: {'primary_action': str, 'secondary_action': str, 'severity': str}
        """
        
        issues = []
        actions = {'primary': None, 'secondary': None, 'severity': 'NORMAL'}
        
        # Check pH issues
        if reading.ph < 6.5:
            issues.append("pH is too low (acidic)")
        elif reading.ph > 8.5:
            issues.append("pH is too high (basic)")
        
        # Check turbidity issues
        if reading.turbidity > 5:
            issues.append("Turbidity is high (water is cloudy)")
        
        # Check TDS issues
        if reading.tds > 500:
            issues.append("TDS is high (too many dissolved solids)")
        
        # Check temperature issues
        if reading.temperature < 10:
            issues.append("Water temperature is too low")
        elif reading.temperature > 40:
            issues.append("Water temperature is too high")
        
        # Check flow rate issues
        if reading.flow_rate < 0.5:
            issues.append("Flow rate is too low")
        elif reading.flow_rate > 10:
            issues.append("Flow rate is too high")
        
        # Determine primary action
        if quality_score < 40:  # Critical
            actions['severity'] = 'CRITICAL'
            actions['primary'] = "STOP WATER USAGE - Activate emergency purification"
            actions['secondary'] = "Check all sensors and filters immediately"
        
        elif quality_score < 60:  # Poor
            actions['severity'] = 'WARNING'
            actions['primary'] = "Increase filtration rate"
            actions['secondary'] = "Reduce water intake or add treatment chemicals"
        
        elif quality_score < 80:  # Fair
            actions['severity'] = 'CAUTION'
            actions['primary'] = "Monitor water quality closely"
            actions['secondary'] = "Prepare for maintenance if needed"
        
        else:  # Good
            actions['severity'] = 'NORMAL'
            actions['primary'] = "System operating normally"
            actions['secondary'] = "Perform routine maintenance checks"
        
        # Override if specific issues exist
        if issues:
            actions['primary'] = f"Address issue: {issues[0]}"
            if len(issues) > 1:
                actions['secondary'] = f"Also address: {issues[1]}"
        
        return {
            'primary_action': actions['primary'],
            'secondary_action': actions['secondary'],
            'severity': actions['severity'],
            'issues': issues
        }


if __name__ == "__main__":
    # Test the purification system
    print("=" * 60)
    print("Purification System Test")
    print("=" * 60)
    
    system = PurificationSystem()
    
    print("\nInitial System Status:")
    print(system.get_system_status())
    
    print("\n[TEST] Activating pump...")
    system.activate_pump()
    print(system.get_system_status())
    
    print("\n[TEST] Deactivating pump...")
    system.deactivate_pump()
    print(system.get_system_status())
    
    print("\n[TEST] Auto-control with quality score 45 (Poor)...")
    system.auto_control(45)
    print(system.get_system_status())
    
    print("\n[TEST] Auto-control with quality score 85 (Good)...")
    system.auto_control(85)
    print(system.get_system_status())
