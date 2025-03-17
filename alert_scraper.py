
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class AlertScraper:
    def __init__(self):
        self.service_updates_url = "https://www.gotransit.com/en/service-updates/service-updates"
        self.main_url = "https://www.gotransit.com/en"
        
    def get_alerts(self):
        """Get alerts from GO Transit website"""
        try:
            alerts = []
            
            # Get service updates
            response = requests.get(self.service_updates_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find alert elements (adjust selectors based on actual page structure)
            alert_elements = soup.select('.service-update, .alert')
            for element in alert_elements:
                alerts.append({
                    'type': 'service_update',
                    'message': element.get_text().strip(),
                    'timestamp': element.select_one('.timestamp').get_text() if element.select_one('.timestamp') else ''
                })
                
            # Get main page alerts
            response = requests.get(self.main_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            alert_elements = soup.select('.alert-banner, .notification')
            for element in alert_elements:
                alerts.append({
                    'type': 'main',
                    'message': element.get_text().strip(),
                    'timestamp': element.select_one('.timestamp').get_text() if element.select_one('.timestamp') else ''
                })
                
            return alerts
            
        except Exception as e:
            logger.error(f"Error fetching alerts: {str(e)}")
            return []

# Create an instance for importing
alert_scraper = AlertScraper()
