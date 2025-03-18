import logging
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def generate_simulated_updates():
    """Generate simulated service updates"""
    base_messages = [
        "GO Transit - All services operating normally",
        "GO Transit - Regular service on all lines",
        "GO Transit - Trains operating on or close to schedule"
    ]
    return [random.choice(base_messages)]

def get_updates():
    """Get simulated service updates"""
    try:
        return generate_simulated_updates()
    except Exception as e:
        logger.error(f"Error generating updates: {str(e)}")
        return ["GO Transit - All services operating normally"]