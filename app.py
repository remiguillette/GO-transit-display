import os
import logging
from datetime import datetime
from flask import Flask, render_template, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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

# Import models after db initialization
from models import Station, Schedule, init_demo_data

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
    language = session.get('language', 'en')
    return render_template('display.html', 
                         station=selected_station,
                         language=language)

@app.route('/control')
def control():
    return render_template('control.html', 
                         stations=STATIONS,
                         selected_station=session.get('selected_station', 'Union'))

@app.route('/api/schedules')
def get_schedules():
    station = request.args.get('station', 'Union')
    try:
        # Get current time
        current_time = datetime.now()

        # Query only future departures
        schedules = Schedule.query.filter(
            Schedule.station == station,
            Schedule.departure_time > current_time
        ).order_by(Schedule.departure_time).limit(8).all()

        schedule_data = []
        for schedule in schedules:
            status = schedule.status
            if status == 'On Time':
                status = schedule.platform if schedule.platform else '-'

            schedule_data.append({
                'departure': schedule.departure_time.strftime('%H:%M'),
                'destination': schedule.destination.upper(),
                'train': f'{schedule.route_code} {schedule.destination}',
                'status': status
            })

        return jsonify(schedule_data)
    except Exception as e:
        logging.error(f"Error fetching schedules: {str(e)}")
        return jsonify({'error': 'Failed to fetch schedules'}), 500

@app.route('/api/set_station', methods=['POST'])
def set_station():
    station = request.form.get('station')
    if station in STATIONS:
        session['selected_station'] = station
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Invalid station'}), 400

@app.route('/api/set_language', methods=['POST'])
def set_language():
    language = request.form.get('language')
    if language in ['en', 'fr']:
        session['language'] = language
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Invalid language'}), 400

# Initialize database and demo data
with app.app_context():
    init_demo_data()