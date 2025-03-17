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
        # You can implement your web scraping logic here to retrieve alerts from the given URL
        # For demonstration purposes, I'm assuming you have a function to scrape alerts from the URL
        # You would replace this with your actual scraping logic
        scraped_alerts = self.scrape_alerts_from_url(url)
        for alert in scraped_alerts:
            self.add_alert(alert['message'], alert['link'])

    def scrape_alerts_from_url(self, url):
        # Implement your web scraping logic here to retrieve alerts from the given URL
        # For demonstration purposes, I'm returning dummy data
        return [
            {'message': 'Alert 1', 'link': 'https://www.gotransit.com/en/service-updates/alert1'},
            {'message': 'Alert 2', 'link': 'https://www.gotransit.com/en/service-updates/alert2'}
        ]

# Create an instance for importing
alert_scraper = AlertScraper()

# Example usage
if __name__ == "__main__":
    url = "https://www.gotransit.com/en/service-updates/service-updates"
    alert_scraper.retrieve_all_alerts(url)
    print(alert_scraper.get_alerts())