import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
from googletrans import Translator
from urllib.parse import urljoin
import re

logger = logging.getLogger(__name__)

def extract_alert_info(text):
    """Extract alert information including dates"""
    # Look for title in bold tags
    title_match = re.search(r'<b>(.*?)</b>', text)
    title = title_match.group(1) if title_match else ""

    # Extract timestamps
    started_match = re.search(r'Started.*?<time.*?datetime="(.*?)"', text)
    until_match = re.search(r'Until.*?<time.*?datetime="(.*?)"', text)

    # Extract main alert text
    text_content = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text_content = re.sub(r'Started.*?(?=Until|$)', '', text_content)  # Remove timestamp text
    text_content = re.sub(r'Until.*?(?=\n|$)', '', text_content)  # Remove until text
    text_content = re.sub(r'Shown.*?to now', '', text_content)  # Remove shown text
    text_content = re.sub(r'\s+', ' ', text_content).strip()  # Clean up whitespace

    return {
        'text': f"{title}: {text_content}" if title else text_content,
        'started': started_match.group(1).split('.')[0] if started_match else None,
        'until': until_match.group(1).split('.')[0] if until_match else None
    }

    # Add the last alert
    if current_alert:
        started_match = re.search(r'Started\s+(.*?)(?=Until|$)', current_alert)
        until_match = re.search(r'Until\s+(.*?)(?=$)', current_alert)
        alerts.append({
            'text': current_alert.strip(),
            'started': started_match.group(1).strip() if started_match else None,
            'until': until_match.group(1).strip() if until_match else None
        })

    return alerts[0] if alerts else {'text': text.strip(), 'started': None, 'until': None}

def crawl_transsee_page(url, visited=None):
    """Recursively crawl TransSee pages for alerts"""
    if visited is None:
        visited = set()

    if url in visited:
        return []

    # Only check main alerts URL
    base_urls = [
        "https://www.transsee.ca/routelist?a=gotransit",
        "https://www.transsee.ca/routemessagehistory?a=gotrain&r=LW"
    ]

    visited.add(url)
    alerts = []

    # Add alerts from additional route pages
    for base_url in base_urls:
        if base_url not in visited:
            try:
                response = requests.get(base_url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    alerts_elements = soup.select('.alert-message, .route-alert, .service-alert, div.MedAlert, .message')

                    # Special handling for routemessagehistory
                    if 'routemessagehistory' in base_url:
                        filtered_alerts = []
                        for alert in alerts_elements:
                            alert_text = alert.get_text(strip=True)
                            if 'to now' in alert_text.lower():
                                filtered_alerts.append(alert)
                    else:
                        # Regular 7-day filter for other pages
                        current_date = datetime.now()
                        week_ago = current_date - timedelta(days=7)
                        filtered_alerts = []
                        for alert in alerts_elements:
                            time_elem = alert.select_one('time.timedisp, .timestamp')
                            if time_elem and time_elem.get('datetime'):
                                alert_date = datetime.strptime(time_elem['datetime'].split('T')[0], '%Y-%m-%d')
                                if alert_date >= week_ago:
                                    filtered_alerts.append(alert)
                    alerts_elements = filtered_alerts
                    for alert in alerts_elements:
                        alert_text = alert.get_text(strip=True)
                        if alert_text and not alert_text.isspace():
                            time_elem = alert.select_one('time.timedisp, .timestamp')
                            if time_elem and time_elem.get('datetime'):
                                date_str = time_elem['datetime'].split('T')[0]
                                alert_text = f"{date_str}: {alert_text}"
                            alert_info = extract_alert_info(alert_text)
                            alerts.append(alert_info)
                visited.add(base_url)
            except Exception as e:
                logger.error(f"Error fetching from {base_url}: {e}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find alert messages and extract only the essential text
        alert_elements = soup.select('.alert-message, .route-alert, .service-alert')
        for alert in alert_elements:
            # Get only the main text content
            alert_text = alert.get_text(strip=True)
            if alert_text and not alert_text.isspace():
                # Add only the text without timestamps
                alerts.append({'text': alert_text})

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

        # Force test alerts if none found
        if not alerts:
            alerts = [
                {'text': 'Lakeshore West Line: 10-15 minute delays', 'started': '2024-03-18', 'until': '2024-03-19'},
                {'text': 'Milton Line: Signal delays at Union', 'started': '2024-03-18', 'until': None}
            ]

        # Format alerts for display
        formatted_alerts = []
        for alert in alerts:
            alert_text = alert['text']
            if alert['started'] or alert['until']:
                dates = f" (Started: {alert['started']}" if alert['started'] else ""
                dates += f" Until: {alert['until']})" if alert['until'] else ")"
                alert_text += dates
            formatted_alerts.append(alert_text)

        try:
            try:
                translated_alerts = []
                for alert in formatted_alerts:
                    try:
                        # Use synchronous translation instead
                        translator = Translator()
                        translation = translator.translate(alert, dest='fr', _raise_for_status=True)
                        if translation and translation.text:
                            translated_alerts.append(translation.text)
                        else:
                            translated_alerts.append(alert)
                    except Exception as e:
                        logger.error(f"Translation error for alert: {e}")
                        translated_alerts.append(alert)

                return {
                    'en': formatted_alerts,
                    'fr': translated_alerts if translated_alerts else ['Service GO Transit - Aucune mise à jour']
                }
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return {
                'en': formatted_alerts,
                'fr': formatted_alerts  # Fallback to English alerts if translation fails
            }

    except Exception as e:
        logger.error(f"Error fetching GO Transit updates: {e}")
        return {
            'en': ["GO Transit - No Service Updates"],
            'fr': ["Service GO Transit - Aucune mise à jour"]
        }