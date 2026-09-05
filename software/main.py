# Smart Water Purification System - Main Application
# This is a placeholder for the main.py file
# Implement Flask app to serve the dashboard and API

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from software.sensors import WaterQualitySensor
from software.purification import PurificationSystem, ActionRecommender
from software.data_processing import WaterQualityAnalyzer, DataStorage
from config import SIMULATION_MODE, SERVER_HOST, SERVER_PORT, DEBUG_MODE
import time

app = Flask(__name__)
CORS(app)

# Initialize components
sensor = WaterQualitySensor(simulation_mode=SIMULATION_MODE)
system = PurificationSystem()
storage = DataStorage()


@app.route('/')
def dashboard():
    """Render main dashboard"""
    reading = sensor.get_all_readings()
    quality_score = WaterQualityAnalyzer.calculate_quality_score(reading)
    status = WaterQualityAnalyzer.get_status(quality_score)
    alert = WaterQualityAnalyzer.get_alert_message(quality_score)
    action = ActionRecommender.get_recommendation(reading, quality_score)
    
    # Get historical data
    history_rows = storage.get_latest_readings(limit=10)
    history = []
    for row in history_rows:
        history.append({
            'label': row[1],  # timestamp
            'ph': row[2],
            'turbidity': row[3],
            'tds': row[4],
            'temperature': row[5],
            'flow': row[6]
        })
    
    return render_template('index.html',
        reading={
            'ph': round(reading.ph, 2),
            'turbidity': round(reading.turbidity, 2),
            'tds': round(reading.tds, 2),
            'flow': round(reading.flow_rate, 2)
        },
        quality={
            'score': quality_score,
            'status': status,
            'alert': alert
        },
        action=action,
        history=history
    )


@app.route('/api/readings/latest')
def api_latest_reading():
    """Get latest sensor reading"""
    reading = sensor.get_all_readings()
    quality_score = WaterQualityAnalyzer.calculate_quality_score(reading)
    status = WaterQualityAnalyzer.get_status(quality_score)
    
    return jsonify({
        'ph': round(reading.ph, 2),
        'turbidity': round(reading.turbidity, 2),
        'tds': round(reading.tds, 2),
        'temperature': round(reading.temperature, 2),
        'flow_rate': round(reading.flow_rate, 2),
        'quality_score': quality_score,
        'status': status,
        'timestamp': reading.timestamp.isoformat()
    })


@app.route('/api/status')
def api_status():
    """Get system status"""
    health = sensor.check_sensor_health()
    system_status = system.get_system_status()
    
    return jsonify({
        'system_online': health['overall'] == 'HEALTHY',
        'pump_active': system_status['pump_active'],
        'sensor_health': health,
        'uptime_seconds': int(time.time())
    })


@app.route('/api/pump/on', methods=['POST'])
def pump_on():
    """Turn on pump"""
    system.activate_pump()
    return jsonify({'success': True, 'message': 'Pump activated'})


@app.route('/api/pump/off', methods=['POST'])
def pump_off():
    """Turn off pump"""
    system.deactivate_pump()
    return jsonify({'success': True, 'message': 'Pump deactivated'})


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("[INFO] Starting Smart Water Purification System...")
    print(f"[INFO] Dashboard available at http://{SERVER_HOST}:{SERVER_PORT}")
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=DEBUG_MODE)
