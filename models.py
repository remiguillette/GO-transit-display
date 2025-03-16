import logging
from datetime import datetime
from db_init import db

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Station(db.Model):
    """Station model representing a GO Transit station"""
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)  # e.g., "ST" for Stouffville
    name = db.Column(db.String(100), nullable=False)
    name_fr = db.Column(db.String(100), nullable=True)
    location_type = db.Column(db.Integer, default=1)  # 1 = station, 0 = stop
    accessible = db.Column(db.Boolean, default=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    lines = db.Column(db.String(100), nullable=True)  # comma-separated line codes
    
    def __repr__(self):
        return f"<Station {self.code} - {self.name}>"

class Schedule(db.Model):
    """Schedule model representing a train schedule entry"""
    id = db.Column(db.Integer, primary_key=True)
    station = db.Column(db.String(100), nullable=False)
    train_number = db.Column(db.String(10), nullable=False)  # e.g., "ST01"
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='On time')  # 'On time', 'Delayed', 'Cancelled'
    platform = db.Column(db.String(5), nullable=True)  # Platform number, e.g., "15"
    route_code = db.Column(db.String(5), nullable=False)  # ST, RH, BR, etc.
    accessible = db.Column(db.Boolean, default=True)
    delay_minutes = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f"<Schedule {self.train_number} - {self.destination} at {self.departure_time}>"

def init_demo_data():
    """Initialize demo data for testing purposes"""
    try:
        # Check if there's any data
        if Station.query.count() > 0:
            logger.info("Database already contains data, skipping initialization")
            return
        
        logger.info("Initializing demo data")
        
        # Create some station entries
        stations = [
            Station(
                code="UN",
                name="Union Station",
                name_fr="Union",
                accessible=True,
                lines="LW,LE,ST,RH,BR,KI,MI"
            ),
            Station(
                code="MI",
                name="Mimico GO",
                name_fr="Mimico",
                accessible=True,
                lines="LW"
            ),
            Station(
                code="EX",
                name="Exhibition GO",
                name_fr="Exhibition",
                accessible=True,
                lines="LW"
            ),
            Station(
                code="PC",
                name="Port Credit GO",
                name_fr="Port Credit",
                accessible=True,
                lines="LW"
            ),
            Station(
                code="AJ",
                name="Ajax GO",
                name_fr="Ajax",
                accessible=True,
                lines="LE"
            ),
            Station(
                code="WH",
                name="Whitby GO",
                name_fr="Whitby",
                accessible=True,
                lines="LE"
            )
        ]
        
        # Add stations to session
        for station in stations:
            db.session.add(station)
        
        # Commit changes
        db.session.commit()
        logger.info(f"Added {len(stations)} stations to the database")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error initializing demo data: {e}")
        raise