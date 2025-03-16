import os
import logging
from datetime import datetime
from flask import Flask, render_template, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Configure PostgreSQL database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

# Import models and scraper after db initialization
from models import Station, Schedule, init_demo_data
from scraper import scraper

# Sample data for stations
STATIONS = {
    "Union": "Toronto Union",
    "Mimico": "Mimico",
    "Exhibition": "Exhibition",
    "Bloor": "Bloor GO"
}

@app.route('/')
def display():
    selected_station = session.get('selected_station', 'Union')
    return render_template('display.html', 
                         station=selected_station)

@app.route('/control')
def control():
    return render_template('control.html', 
                         stations=STATIONS,
                         selected_station=session.get('selected_station', 'Union'))

@app.route('/api/schedules')
def get_schedules():
    station = request.args.get('station', 'Union')
    try:
        # Get schedules from scraper
        schedule_data = scraper.get_station_schedule(station)

        # Format schedules for display
        formatted_schedules = []
        for schedule in schedule_data:
            status = schedule['status']
            if status == 'On Time':
                status = schedule['platform'] if schedule['platform'] else '-'

            formatted_schedules.append({
                'departure': schedule['departure_time'].strftime('%H:%M'),
                'destination': schedule['destination'].upper(),
                'train': f"{schedule['route_code']} {schedule['destination']}",
                'status': status
            })

        return jsonify(formatted_schedules)
    except Exception as e:
        logger.error(f"Error fetching schedules: {str(e)}")
        return jsonify({'error': 'Failed to fetch schedules'}), 500

@app.route('/api/set_station', methods=['POST'])
def set_station():
    station = request.form.get('station')
    if station in STATIONS:
        session['selected_station'] = station
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Invalid station'}), 400

# Initialize database and demo data
with app.app_context():
    init_demo_data()