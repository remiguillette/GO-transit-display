import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from datetime import datetime
import scraper


# Configure logging
logging.basicConfig(level=logging.DEBUG)


# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")


# Default station to display
DEFAULT_STATION = "Union"


@app.route('/')
def index():
    """Main display board route"""
    # Get selected station from session or use default
    selected_station = session.get('selected_station', DEFAULT_STATION)
    
    # Get the current schedule for the selected station
    station_data = scraper.get_station_schedule(selected_station)
    
    # Get the current time for display with seconds
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Get the list of available stations for the dropdown
    stations = scraper.get_available_stations()
    
    return render_template('index.html', 
                          station=selected_station,
                          schedule=station_data,
                          current_time=current_time,
                          stations=stations)


@app.route('/control')
def control():
    """Control panel for station selection"""
    # Get the current selected station
    selected_station = session.get('selected_station', DEFAULT_STATION)
    
    # Get the list of available stations
    stations = scraper.get_available_stations()
    
    return render_template('control.html',
                          selected_station=selected_station,
                          stations=stations)


@app.route('/set_station', methods=['POST'])
def set_station():
    """Set the station for display"""
    station = request.form.get('station')
    if station:
        session['selected_station'] = station
        return redirect(url_for('index'))
    return redirect(url_for('control'))


@app.route('/schedule')
def schedule():
    """API endpoint to get the current schedule data (for AJAX updates)"""
    selected_station = session.get('selected_station', DEFAULT_STATION)
    station_data = scraper.get_station_schedule(selected_station)
    return render_template('schedule_partial.html', 
                          station=selected_station,
                          schedule=station_data)


@app.route('/current_time')
def current_time():
    """API endpoint to get the current time (for AJAX updates)"""
    current = datetime.now().strftime("%H:%M:%S")
    return jsonify({"time": current})


@app.route('/api/schedule')
def api_schedule():
    """JSON API for schedule data"""
    selected_station = session.get('selected_station', DEFAULT_STATION)
    station_data = scraper.get_station_schedule(selected_station)
    return jsonify(station_data)


@app.context_processor
def utility_processor():
    """Add utility functions for templates"""
    def get_line_color(line_code):
        return scraper.get_line_color(line_code)
    
    def format_time(time_str):
        # Format time for display
        return time_str
    
    return {
        'get_line_color': get_line_color,
        'format_time': format_time
    }
from app import app


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)