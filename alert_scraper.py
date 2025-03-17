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

    def remove_alert(self, message):
        """Remove an alert by message"""
        self.alerts = [alert for alert in self.alerts if alert['message'] != message]

    def get_alerts(self):
        """Get all current alerts"""
        return self.alerts

    def clear_alerts(self):
        """Clear all alerts"""
        self.alerts = []

# Create an instance for importing
alert_scraper = AlertScraper()

# Add some default alerts for testing
alert_scraper.add_alert("Welcome to GO Transit Display", "info")