from datetime import datetime
from app import db

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    name_fr = db.Column(db.String(100), nullable=False)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station = db.Column(db.String(100), nullable=False)
    train_number = db.Column(db.String(10), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='On Time')
    track = db.Column(db.String(5))
