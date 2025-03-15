from datetime import datetime
from app import db

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)  # e.g., "ST" for Stouffville
    name = db.Column(db.String(100), nullable=False)
    name_fr = db.Column(db.String(100), nullable=False)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station = db.Column(db.String(100), nullable=False)
    train_number = db.Column(db.String(10), nullable=False)  # e.g., "ST01"
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='On Time')  # 'On Time', 'DELAYED', 'CANCELLED'
    platform = db.Column(db.String(5))  # Platform number, e.g., "15"
    route_code = db.Column(db.String(5), nullable=False)  # ST, RH, BR, etc.

# Initialize demo data
def init_demo_data():
    db.drop_all()
    db.create_all()

    # Add stations
    stations = [
        Station(code='ST', name='Stouffville', name_fr='Stouffville'),
        Station(code='RH', name='Richmond Hill', name_fr='Richmond Hill'),
        Station(code='BR', name='Barrie', name_fr='Barrie')
    ]
    db.session.bulk_save_objects(stations)

    # Add schedules
    current_time = datetime.now()
    schedules = [
        Schedule(
            station='Union',
            train_number='ST01',
            destination='Stouffville',
            departure_time=datetime.strptime(f"{current_time.date()} 06:33", "%Y-%m-%d %H:%M"),
            status='On Time',
            platform='15',
            route_code='ST'
        ),
        Schedule(
            station='Union',
            train_number='ST02',
            destination='Stouffville',
            departure_time=datetime.strptime(f"{current_time.date()} 07:16", "%Y-%m-%d %H:%M"),
            status='DELAYED',
            platform=None,
            route_code='ST'
        ),
        Schedule(
            station='Union',
            train_number='RH01',
            destination='Richmond Hill',
            departure_time=datetime.strptime(f"{current_time.date()} 07:17", "%Y-%m-%d %H:%M"),
            status='On Time',
            platform='12',
            route_code='RH'
        ),
        Schedule(
            station='Union',
            train_number='BR01',
            destination='Barrie',
            departure_time=datetime.strptime(f"{current_time.date()} 07:41", "%Y-%m-%d %H:%M"),
            status='DELAYED',
            platform=None,
            route_code='BR'
        ),
        Schedule(
            station='Union',
            train_number='ST03',
            destination='Stouffville',
            departure_time=datetime.strptime(f"{current_time.date()} 08:03", "%Y-%m-%d %H:%M"),
            status='CANCELLED',
            platform=None,
            route_code='ST'
        )
    ]
    db.session.bulk_save_objects(schedules)
    db.session.commit()