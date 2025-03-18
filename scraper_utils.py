
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def get_go_transit_updates():
    """Fetch GO Transit service updates from TransSee"""
    try:
        # Get the service updates from TransSee
        url = "https://www.transsee.ca/routelist?a=gotransit"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find service alerts
        alerts = []
        
        # Look for alert elements
        alert_elements = soup.select('.alert, .service-alert')
        if alert_elements:
            for alert in alert_elements:
                alert_text = alert.get_text(strip=True)
                if alert_text:
                    alerts.append(alert_text)
        
        if not alerts:
            alerts = ["GO Transit - All services operating normally"]
            
        return alerts

    except Exception as e:
        logger.error(f"Error fetching GO Transit updates: {e}")
        return ["GO Transit - No Service Updates"]
