import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Set up the DeclarativeBase
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with our base
db = SQLAlchemy(model_class=Base)

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure secret key
    app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")
    
    # Configure database connection
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///gotransit.db")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    # Initialize the database with the app
    db.init_app(app)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(os.path.join(app.instance_path), exist_ok=True)
    except OSError:
        pass
    
    return app