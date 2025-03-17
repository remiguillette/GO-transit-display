
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AlertScraper:
    def __init__(self):
        self.alerts = []

    def add_alert(self, message, link, alert_type="service_update"):
        """
        Add a new alert

        Args:
            message (str): The alert message.
            link (str): The link to the alert.
            alert_type (str, optional): The type of alert. Defaults to "service_update".
        """
        self.alerts.append({
            'type': alert_type,
            'message': message,
            'link': link,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    def remove_alert(self, message):
        """
        Remove an alert by message

        Args:
            message (str): The message of the alert to be removed.
        """
        self.alerts = [alert for alert in self.alerts if alert['message'] != message]

    def get_alert(self, link):
        """
        Get an alert by link

        Args:
            link (str): The link of the alert to be retrieved.

        Returns:
            dict: The alert dictionary if found, otherwise None.
        """
        for alert in self.alerts:
            if alert['link'] == link:
                return alert
        return None

    def get_alerts(self):
        """
        Get all current alerts

        Returns:
            list: A list of alert dictionaries.
        """
        if not self.alerts:
            self.add_alert("Welcome to GO Transit", "https://www.gotransit.com", "info")
            self.retrieve_all_alerts("https://www.gotransit.com/en/service-updates/service-updates")
        return self.alerts

    def clear_alerts(self):
        """
        Clear all alerts
        """
        self.alerts = []

    def retrieve_all_alerts(self, url):
        """
        Retrieve all alerts from the given URL

        Args:
            url (str): The URL to retrieve alerts from.
        """
        self.clear_alerts()
        scraped_alerts = self.scrape_alerts_from_url(url)
        for alert in scraped_alerts:
            self.add_alert(alert['message'], alert['link'])

    def scrape_alerts_from_url(self, url):
        """Scrape service updates from GO Transit website"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            alerts = []
            
            # Find service updates using broader selectors
            update_containers = soup.find_all(['div', 'article'], class_=['service-update-container', 'service-update', 'alert'])
            
            for container in update_containers:
                link_elem = container.find('a')
                message_elem = container.find(['div', 'p'], class_=['message', 'description', 'alert-text'])
                
                link = ''
                if link_elem:
                    link = link_elem.get('href', '')
                    if not link.startswith('http'):
                        link = 'https://www.gotransit.com' + link
                
                message = message_elem.get_text(strip=True) if message_elem else container.get_text(strip=True)
                if message:
                    alerts.append({
                        'message': message,
                        'link': link
                    })
            
            logger.info(f"Scraped {len(alerts)} alerts from GO Transit website")
            return alerts
            
        except Exception as e:
            logger.error(f"Error scraping alerts: {str(e)}")
            return []

# Create an instance for importing
alert_scraper = AlertScraper()

# Example usage
if __name__ == "__main__":
    url = "https://www.gotransit.com/en/service-updates/service-updates"
    alert_scraper.retrieve_all_alerts(url)
    print(alert_scraper.get_alerts())
