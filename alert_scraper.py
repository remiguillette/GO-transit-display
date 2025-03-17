
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime

logger = logging.getLogger(__name__)

class AlertScraper:
    def __init__(self):
        self.alerts = []
        self.urls = [
            'https://www.gotransit.com/en',
            'https://www.gotransit.com/en/service-updates/service-updates'
        ]

    def scrape_alerts(self):
        """Scrape alerts from GO Transit websites"""
        for url in self.urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find service updates and alerts
                alerts = soup.find_all(['div', 'section'], class_=['alert', 'service-update'])
                
                for alert in alerts:
                    message = alert.get_text().strip()
                    if message:
                        self.add_alert(message, 'service_update')
                        
            except Exception as e:
                logger.error(f"Error scraping alerts from {url}: {str(e)}")

    def add_alert(self, message, alert_type="service_update"):
        """Add a new alert"""
        self.alerts.append({
            'type': alert_type,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    def get_alerts(self):
        """Get all current alerts"""
        self.scrape_alerts()  # Refresh alerts before returning
        return self.alerts

    def clear_alerts(self):
        """Clear all alerts"""
        self.alerts = []

# Create an instance for importing
alert_scraper = AlertScraper()
