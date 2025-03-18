
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class TransSeeScraper:
    def __init__(self):
        self.base_urls = [
            'https://www.transsee.ca/stoplist?a=gotrain&r=BR',
            'https://www.transsee.ca/stoplist?a=gotrain&r=GT',
            'https://www.transsee.ca/stoplist?a=gotrain&r=LE',
            'https://www.transsee.ca/stoplist?a=gotrain&r=LW',
            'https://www.transsee.ca/routemessagehistory?a=gotrain&r=LW'
        ]
        self.alerts = []
        self.footer = '---\nScraper by [Your Name]'  # Keep this as is

    def fetch_data(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None

    def parse_alerts(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        alerts = []
        now = datetime.now()
        seven_days_ago = now - timedelta(days=7)

        # Find all relevant messages and dates
        messages = soup.find_all('div', class_='message')  # Adjust the class name if needed
        for message in messages:
            date_str = message.find('span', class_='date').text.strip()  # Adjust if different structure
            message_text = message.text.strip()

            try:
                alert_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                if seven_days_ago <= alert_date <= now:
                    alerts.append(message_text)
            except ValueError:
                continue

        return alerts

    def get_go_transit_updates(self):
        """Get GO Transit service updates"""
        all_alerts = []
        for url in self.base_urls:
            html_content = self.fetch_data(url)
            if html_content:
                alerts = self.parse_alerts(html_content)
                all_alerts.extend(alerts)
        return list(set(all_alerts))  # Remove duplicates

    def scrape(self):
        """Main scraping method"""
        self.alerts = self.get_go_transit_updates()

    def display_alerts(self):
        """Display all alerts"""
        print('Service Alerts from TransSee (Last 7 Days):')
        for alert in self.alerts:
            print(f'- {alert}')
        print(self.footer)

def get_go_transit_updates():
    """Get GO Transit service updates"""
    scraper = TransSeeScraper()
    scraper.scrape()
    return scraper.alerts

# Create an instance for importing
scraper = TransSeeScraper()

if __name__ == '__main__':
    scraper = TransSeeScraper()
    scraper.scrape()
    scraper.display_alerts()
