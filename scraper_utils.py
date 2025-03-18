
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from urllib.parse import urljoin
import re

logger = logging.getLogger(__name__)

def extract_alert_info(text):
    """Extract alert information including dates"""
    started_match = re.search(r'Started\s+(.*?)(?=Until|$)', text)
    until_match = re.search(r'Until\s+(.*?)(?=$|\n)', text)
    
    started = started_match.group(1).strip() if started_match else None
    until = until_match.group(1).strip() if until_match else None
    
    return {
        'text': text.strip(),
        'started': started,
        'until': until
    }

def crawl_transsee_page(url, visited=None):
    """Recursively crawl TransSee pages for alerts"""
    if visited is None:
        visited = set()
    
    if url in visited:
        return []
    
    visited.add(url)
    alerts = []
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find MedAlert service alerts
        med_alerts = soup.select('div.MedAlert')
        for alert in med_alerts:
            alert_text = alert.get_text(strip=True)
            if alert_text and not alert_text.isspace():
                # Extract time elements
                time_elem = alert.select_one('time.timedisp')
                if time_elem:
                    started = time_elem.get('datetime', '').split('T')[0]
                else:
                    started = None
                
                # Look for "Until" text
                until_text = alert.text
                until_match = re.search(r'Until\s+(.*?)(?=\s|$)', until_text)
                until = until_match.group(1) if until_match else None
                
                alert_info = {
                    'text': alert_text,
                    'started': started,
                    'until': until
                }
                alerts.append(alert_info)

        # Check embedded service update links
        update_links = soup.select('a[href*="service-updates"]')
        for link in update_links[:3]:  # Limit to 3 to avoid too many requests
            next_url = urljoin(url, link['href'])
            if next_url not in visited:
                alerts.extend(crawl_transsee_page(next_url, visited))
                
        # Also check message history
        history_links = soup.select('a[href*="routemessagehistory"]')
        for link in history_links[:3]:  # Limit to first 3 routes to avoid too many requests
            history_url = urljoin(url, link['href'])
            if history_url not in visited:
                try:
                    history_response = requests.get(history_url, timeout=10)
                    history_soup = BeautifulSoup(history_response.text, 'html.parser')
                    history_alerts = history_soup.select('.message-text, .route-message')
                    for alert in history_alerts:
                        alert_text = alert.get_text(strip=True)
                        if alert_text and not alert_text.isspace():
                            alert_info = extract_alert_info(alert_text)
                            alerts.append(alert_info)
                except Exception as e:
                    logger.error(f"Error fetching history from {history_url}: {e}")
        
        # Find "More..." links and follow them
        more_links = soup.find_all('a', string=re.compile(r'More\.{3}|More$', re.I))
        for link in more_links:
            next_url = urljoin(url, link.get('href'))
            if next_url not in visited:
                alerts.extend(crawl_transsee_page(next_url, visited))
                
        # Look for route-specific links
        route_links = soup.select('a[href*="routemessagehistory"]')
        for link in route_links:
            next_url = urljoin(url, link.get('href'))
            if next_url not in visited:
                alerts.extend(crawl_transsee_page(next_url, visited))
                
    except Exception as e:
        logger.error(f"Error crawling {url}: {e}")
    
    return alerts

def get_go_transit_updates():
    """Fetch GO Transit service updates from TransSee"""
    try:
        base_url = "https://www.transsee.ca/routelist?a=gotransit"
        alerts = crawl_transsee_page(base_url)
        
        if not alerts:
            return ["GO Transit - All services operating normally"]
            
        # Format alerts for display
        formatted_alerts = []
        for alert in alerts:
            alert_text = alert['text']
            if alert['started'] or alert['until']:
                dates = f" (Started: {alert['started']}" if alert['started'] else ""
                dates += f" Until: {alert['until']})" if alert['until'] else ")"
                alert_text += dates
            formatted_alerts.append(alert_text)
            
        return formatted_alerts

    except Exception as e:
        logger.error(f"Error fetching GO Transit updates: {e}")
        return ["GO Transit - No Service Updates"]
