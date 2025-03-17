import os
import logging
import time
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, jsonify, request, session, Response, stream_with_context
from flask_socketio import SocketIO, emit
from db_init import create_app, db

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*")

# Import models and data modules after db initialization to avoid circular imports
from models import Station, Schedule
import sys
sys.path.append('.')  # Ensure the current directory is in the path
from gtfs_parser import gtfs_data
from go_scraper import scraper

# Configure socket logging
socketio.logger.setLevel(logging.ERROR)
engineio_logger = logging.getLogger('engineio')
engineio_logger.setLevel(logging.ERROR)

# Make sure GTFS data is loaded
gtfs_data.load_data()

# Rate limiting implementation
class RateLimiter:
    def __init__(self, limit=30, window=60):
        self.limit = limit  # Number of requests allowed
        self.window = window  # Time window in seconds
        self.clients = {}  # {ip: [timestamps]}

    def is_rate_limited(self, ip):
        current_time = time.time()

        # If client IP not in dictionary, add it
        if ip not in self.clients:
            self.clients[ip] = []

        # Clean up old timestamps
        self.clients[ip] = [t for t in self.clients[ip] if current_time - t < self.window]

        # Check if rate limit exceeded
        if len(self.clients[ip]) >= self.limit:
            return True

        # Add current timestamp
        self.clients[ip].append(current_time)
        return False

# Create rate limiter instances
api_limiter = RateLimiter(limit=60, window=60)  # 60 requests per minute for API
sse_limiter = RateLimiter(limit=10, window=60)  # 10 SSE connections per minute

# Rate limit decorator
def rate_limit(limiter):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            client_ip = request.remote_addr

            if limiter.is_rate_limited(client_ip):
                return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429

            return f(*args, **kwargs)
        return wrapped
    return decorator

@app.route('/')
def display():
    """Main display board route"""
    selected_station = session.get('selected_station', 'Union Station')
    return render_template('display.html', 
                         station=selected_station)

@app.route('/control')
def control():
    """Control panel for station selection"""
    # Get station list from GTFS data
    stations = {}
    for station_name in scraper.get_available_stations():
        # Remove " GO" from station names for cleaner display
        display_name = station_name.replace(" GO", "") if station_name.endswith(" GO") else station_name
        stations[station_name] = display_name

    return render_template('control.html', 
                         stations=stations,
                         selected_station=session.get('selected_station', 'Union Station'))

@app.route('/api/schedules')
def get_schedules():
    """API endpoint to get the current schedule data (for AJAX updates)"""
    station = request.args.get('station', 'Union Station')
    try:
        # Get schedules from scraper
        schedule_data = scraper.get_station_schedule(station)

        # Format schedules for display
        formatted_schedules = []
        for schedule in schedule_data:
            status = schedule['status']
            if status == 'On time':
                status = schedule['platform'] if schedule['platform'] else '-'

            # Format the time from datetime object
            departure_time = schedule['departure_time'].strftime('%H:%M')

            formatted_schedules.append({
                'departure': departure_time,
                'destination': schedule['destination'].upper(),
                'train': f"{schedule['route_code']} {schedule['destination']}",
                'status': status,
                'color': schedule['color'],
                'accessible': schedule['accessible']
            })

        return jsonify(formatted_schedules)
    except Exception as e:
        logger.error(f"Error fetching schedules: {str(e)}")
        return jsonify({'error': 'Failed to fetch schedules'}), 500

@app.route('/api/set_station', methods=['POST'])
@rate_limit(api_limiter)
def set_station():
    """Set the station for display"""
    station = request.form.get('station')
    if station in scraper.get_available_stations():
        session['selected_station'] = station
        # Emit station update via WebSocket
        socketio.emit('station_update', {'station': station})
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Invalid station'}), 400

@app.route('/api/sse/station_updates')
@rate_limit(sse_limiter)
def sse_station_updates():
    """Server-Sent Events endpoint for real-time station updates"""
    def event_stream():
        # Send initial event
        yield f"data: {{'event': 'connected'}}\n\n"

        # Keep the connection alive
        while True:
            # Check if session has a selected station
            station = session.get('selected_station', 'Union Station')

            # Send station update every 5 seconds
            yield f"data: {{'event': 'station_update', 'station': '{station}'}}\n\n"
            time.sleep(5)  # Sleep to avoid too frequent updates

    response = Response(stream_with_context(event_stream()),
                      mimetype="text/event-stream")
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['X-Accel-Buffering'] = 'no'
    return response

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    logger.debug('Client connected via WebSocket')

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    logger.debug('Client disconnected from WebSocket')

@socketio.on('request_station')
def handle_station_request():
    """Handle request for current station via WebSocket"""
    station = session.get('selected_station', 'Union Station')
    emit('station_update', {'station': station})

@app.route('/api/stations')
def get_stations():
    """API endpoint to get the list of available stations"""
    stations = scraper.get_available_stations()
    return jsonify(stations)

@app.route('/api/current_time')
def current_time():
    """API endpoint to get the current time (for AJAX updates)"""
    return jsonify({
        'time': datetime.now().strftime('%H:%M:%S'),
        'date': datetime.now().strftime('%Y-%m-%d')
    })

@app.route('/api/schedule', methods=['GET'])
def api_schedule():
    """JSON API for schedule data"""
    station = request.args.get('station', 'Union Station')

    try:
        schedule_data = scraper.get_station_schedule(station)
        return jsonify(schedule_data)
    except Exception as e:
        logger.error(f"Error in API: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Initialize database
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        logger.error(f"Database initialization error: {e}")

# Enable CORS for development
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)