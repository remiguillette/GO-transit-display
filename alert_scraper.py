
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AlertScraper:
    def __init__(self):
        self.alerts = []

    def add_alert(self, message, alert_type="service_update"):
        """Add a new alert"""
        self.alerts.append({
            'type': alert_type,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    def get_alerts(self):
        """Get all current alerts"""
        return self.alerts

# Create an instance for importing
alert_scraper = AlertScraper()
