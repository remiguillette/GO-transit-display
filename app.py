import os
import logging
from datetime import datetime
from flask import Flask, render_template, jsonify, request, session
from db_init import create_app, db

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = create_app()

# Import models and data modules after db initialization to avoid circular imports
from models import Station, Schedule
import sys
sys.path.append('.')  # Ensure the current directory is in the path
from gtfs_parser import gtfs_data
from go_scraper import scraper

# Make sure GTFS data is loaded
gtfs_data.load_data()

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
def set_station():
    """Set the station for display"""
    station = request.form.get('station')
    if station in scraper.get_available_stations():
        session['selected_station'] = station
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Invalid station'}), 400

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