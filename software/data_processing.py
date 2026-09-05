# Data Processing Module
# Handles quality scoring, analysis, and reporting

import sqlite3
from datetime import datetime, timedelta
from config import (
    PH_WEIGHT, TURBIDITY_WEIGHT, TDS_WEIGHT, TEMP_WEIGHT, FLOW_WEIGHT,
    QUALITY_SCORE_GOOD, QUALITY_SCORE_FAIR, QUALITY_SCORE_POOR,
    LOCAL_DB_PATH, PH_ALERT_MIN, PH_ALERT_MAX, TURBIDITY_ALERT_THRESHOLD,
    TDS_ALERT_THRESHOLD, TEMP_ALERT_MIN, TEMP_ALERT_MAX
)


class WaterQualityAnalyzer:
    """Analyze water quality readings and generate scores"""
    
    @staticmethod
    def calculate_quality_score(reading):
        """
        Calculate overall water quality score (0-100)
        Based on weighted parameters
        """
        
        # Calculate individual parameter scores (0-100)
        ph_score = WaterQualityAnalyzer._score_ph(reading.ph)
        turbidity_score = WaterQualityAnalyzer._score_turbidity(reading.turbidity)
        tds_score = WaterQualityAnalyzer._score_tds(reading.tds)
        temp_score = WaterQualityAnalyzer._score_temperature(reading.temperature)
        flow_score = WaterQualityAnalyzer._score_flow(reading.flow_rate)
        
        # Calculate weighted average
        total_weight = PH_WEIGHT + TURBIDITY_WEIGHT + TDS_WEIGHT + TEMP_WEIGHT + FLOW_WEIGHT
        
        quality_score = (
            (ph_score * PH_WEIGHT +
             turbidity_score * TURBIDITY_WEIGHT +
             tds_score * TDS_WEIGHT +
             temp_score * TEMP_WEIGHT +
             flow_score * FLOW_WEIGHT) / total_weight
        )
        
        return round(quality_score, 2)
    
    @staticmethod
    def _score_ph(ph):
        """Score pH level (0-100)"""
        # Ideal range: 6.5-8.5
        if 6.5 <= ph <= 8.5:
            return 100
        elif ph < 6.5:
            # Below ideal - deduct points linearly
            return max(0, 100 - (6.5 - ph) * 10)
        else:
            # Above ideal - deduct points linearly
            return max(0, 100 - (ph - 8.5) * 10)
    
    @staticmethod
    def _score_turbidity(turbidity):
        """Score turbidity level (0-100)"""
        # Ideal: < 5 NTU
        if turbidity <= 5:
            return 100
        elif turbidity <= 10:
            return 80
        elif turbidity <= 20:
            return 50
        elif turbidity <= 50:
            return 30
        else:
            return max(0, 100 - turbidity * 2)
    
    @staticmethod
    def _score_tds(tds):
        """Score TDS level (0-100) - ppm"""
        # Ideal: < 500 ppm
        if tds <= 500:
            return 100
        elif tds <= 750:
            return 75
        elif tds <= 1000:
            return 50
        else:
            return max(0, 100 - (tds - 1000) * 0.05)
    
    @staticmethod
    def _score_temperature(temp):
        """Score temperature level (0-100)"""
        # Ideal: 10-40°C
        if 10 <= temp <= 40:
            return 100
        elif temp < 10:
            return max(0, 100 - (10 - temp) * 5)
        else:
            return max(0, 100 - (temp - 40) * 5)
    
    @staticmethod
    def _score_flow(flow_rate):
        """Score flow rate (0-100) - L/min"""
        # Ideal: 0.5-10 L/min
        if 0.5 <= flow_rate <= 10:
            return 100
        elif flow_rate < 0.5:
            return max(0, 100 - (0.5 - flow_rate) * 50)
        else:
            return max(0, 100 - (flow_rate - 10) * 5)
    
    @staticmethod
    def get_status(quality_score):
        """Get quality status based on score"""
        if quality_score >= QUALITY_SCORE_GOOD:
            return 'Good'
        elif quality_score >= QUALITY_SCORE_FAIR:
            return 'Fair'
        elif quality_score >= QUALITY_SCORE_POOR:
            return 'Poor'
        else:
            return 'Critical'
    
    @staticmethod
    def get_alert_message(quality_score):
        """Get alert message based on quality score"""
        if quality_score >= QUALITY_SCORE_GOOD:
            return 'Water is safe for consumption'
        elif quality_score >= QUALITY_SCORE_FAIR:
            return 'Water quality is acceptable - Monitor closely'
        elif quality_score >= QUALITY_SCORE_POOR:
            return 'Water quality is poor - Treatment recommended'
        else:
            return 'CRITICAL - Water is unsafe - Stop usage immediately'


class DataStorage:
    """Handle local database storage and retrieval"""
    
    def __init__(self, db_path=LOCAL_DB_PATH):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database with required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create readings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ph REAL,
                    turbidity REAL,
                    tds REAL,
                    temperature REAL,
                    flow_rate REAL,
                    quality_score REAL,
                    status TEXT
                )
            ''')
            
            # Create alerts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    alert_type TEXT,
                    severity TEXT,
                    message TEXT,
                    read INTEGER DEFAULT 0
                )
            ''')
            
            # Create maintenance log table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS maintenance_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    maintenance_type TEXT,
                    description TEXT,
                    duration_seconds INTEGER
                )
            ''')
            
            conn.commit()
            conn.close()
            print("[INFO] Database initialized successfully")
        
        except Exception as e:
            print(f"[ERROR] Database initialization failed: {e}")
    
    def save_reading(self, reading, quality_score, status):
        """Save sensor reading to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO readings 
                (ph, turbidity, tds, temperature, flow_rate, quality_score, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                reading.ph, reading.turbidity, reading.tds,
                reading.temperature, reading.flow_rate,
                quality_score, status
            ))
            
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"[ERROR] Failed to save reading: {e}")
            return False
    
    def get_latest_readings(self, limit=100):
        """Retrieve latest readings from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM readings
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return rows
        
        except Exception as e:
            print(f"[ERROR] Failed to retrieve readings: {e}")
            return []
    
    def get_readings_since(self, hours=24):
        """Get readings from the last N hours"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            time_threshold = datetime.now() - timedelta(hours=hours)
            
            cursor.execute('''
                SELECT * FROM readings
                WHERE timestamp > ?
                ORDER BY timestamp DESC
            ''', (time_threshold,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return rows
        
        except Exception as e:
            print(f"[ERROR] Failed to retrieve readings: {e}")
            return []
    
    def save_alert(self, alert_type, severity, message):
        """Save alert to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO alerts (alert_type, severity, message)
                VALUES (?, ?, ?)
            ''', (alert_type, severity, message))
            
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"[ERROR] Failed to save alert: {e}")
            return False
    
    def log_maintenance(self, maintenance_type, description, duration=0):
        """Log maintenance activity"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO maintenance_log (maintenance_type, description, duration_seconds)
                VALUES (?, ?, ?)
            ''', (maintenance_type, description, duration))
            
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"[ERROR] Failed to log maintenance: {e}")
            return False
    
    def get_statistics(self, hours=24):
        """Get statistics for the last N hours"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            time_threshold = datetime.now() - timedelta(hours=hours)
            
            cursor.execute('''
                SELECT 
                    AVG(ph) as avg_ph,
                    MIN(ph) as min_ph,
                    MAX(ph) as max_ph,
                    AVG(turbidity) as avg_turbidity,
                    AVG(tds) as avg_tds,
                    AVG(temperature) as avg_temp,
                    AVG(quality_score) as avg_quality,
                    COUNT(*) as reading_count
                FROM readings
                WHERE timestamp > ?
            ''', (time_threshold,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'avg_ph': round(result[0], 2) if result[0] else 0,
                    'min_ph': round(result[1], 2) if result[1] else 0,
                    'max_ph': round(result[2], 2) if result[2] else 0,
                    'avg_turbidity': round(result[3], 2) if result[3] else 0,
                    'avg_tds': round(result[4], 2) if result[4] else 0,
                    'avg_temp': round(result[5], 2) if result[5] else 0,
                    'avg_quality': round(result[6], 2) if result[6] else 0,
                    'reading_count': result[7]
                }
            
            return None
        
        except Exception as e:
            print(f"[ERROR] Failed to get statistics: {e}")
            return None


if __name__ == "__main__":
    # Test data processing
    print("=" * 60)
    print("Data Processing Test")
    print("=" * 60)
    
    # Create a mock reading
    class MockReading:
        def __init__(self):
            self.ph = 7.2
            self.turbidity = 2.5
            self.tds = 300
            self.temperature = 25
            self.flow_rate = 3.5
    
    reading = MockReading()
    score = WaterQualityAnalyzer.calculate_quality_score(reading)
    status = WaterQualityAnalyzer.get_status(score)
    alert = WaterQualityAnalyzer.get_alert_message(score)
    
    print(f"\nQuality Score: {score}/100")
    print(f"Status: {status}")
    print(f"Alert: {alert}")
    
    # Test database
    storage = DataStorage()
    storage.save_reading(reading, score, status)
    print("\n[INFO] Reading saved to database")
