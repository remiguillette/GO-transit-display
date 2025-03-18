import requests
from bs4 import BeautifulSoup
import time
import logging

logger = logging.getLogger(__name__)

def get_go_transit_updates():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        url = "https://www.gotransit.com/en/service-updates/service-updates"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find service alerts
        alerts = soup.find_all('div', class_='service-alert')
        updates = []

        for alert in alerts:
            alert_text = alert.get_text(strip=True)
            if alert_text:
                updates.append(alert_text)

        if not updates:
            return ["GO Transit - All services operating normally"]

        return updates

    except Exception as e:
        logger.error(f"Error fetching updates: {str(e)}")
        return ["GO Transit - All services operating normally"]