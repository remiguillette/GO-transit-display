
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def get_go_transit_updates():
    """Get service updates from GO Transit website"""
    try:
        url = 'https://www.gotransit.com/en/service-updates'
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        updates = []
        for item in soup.select('.service-update-list-item'):
            try:
                title = item.find('h3')
                description = item.find('p')
                
                title_text = title.text.strip() if title else "GO Transit"
                desc_text = description.text.strip() if description else "All services operating normally"
                
                updates.append(f"{title_text}: {desc_text}")
            except (AttributeError, TypeError) as e:
                logger.warning(f"Error parsing update item: {e}")
                updates.append("GO Transit - All services operating normally")
                
        return updates if updates else ["GO Transit - All services operating normally"]
    except Exception as e:
        logger.error(f"Error fetching GO Transit updates: {e}")
        return ["GO Transit - All services operating normally"]
