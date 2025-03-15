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

# Configure SQLite database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gotransit.db"
db.init_app(app)

# Import models after db initialization
from models import Station, Schedule

# Sample data for stations
STATIONS = {
    "Union": "Toronto Union",
    "Mimico": "Mimico",
    "Exhibition": "Exhibition",
    "Bloor": "Bloor GO"
}

# Route handlers
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
    schedules = Schedule.query.filter_by(station=station).all()
    current_time = datetime.now()
    
    schedule_data = []
    for schedule in schedules:
        if schedule.departure_time > current_time:
            schedule_data.append({
                'train': schedule.train_number,
                'destination': schedule.destination,
                'departure': schedule.departure_time.strftime('%H:%M'),
                'status': schedule.status,
                'track': schedule.track
            })
    
    return jsonify(schedule_data)

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

# Initialize database
with app.app_context():
    db.create_all()
