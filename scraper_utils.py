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

def crawl_transsee_page(url, visited=None):
    """Recursively crawl TransSee pages for alerts"""
    if visited is None:
        visited = set()

    # Return demo alerts instead of scraping
    return [
        {'text': 'Lakeshore West Line: 10-15 minute delays', 'started': '2024-03-18', 'until': '2024-03-19'},
        {'text': 'Milton Line: Signal delays at Union', 'started': '2024-03-18', 'until': None}
    ]

def get_go_transit_updates():
    """Fetch GO Transit service updates"""
    try:
        # Return demo alerts instead of scraping
        alerts = {
            'en': [
                'Lakeshore West Line: 10-15 minute delays',
                'Milton Line: Signal delays at Union'
            ],
            'fr': [
                'Ligne Lakeshore West: retards de 10-15 minutes',
                'Ligne Milton: retards de signalisation à Union'
            ]
        }
        return alerts
    except Exception as e:
        logger.error(f"Error fetching GO Transit updates: {e}")
        return {
            'en': ["GO Transit - No Service Updates"],
            'fr': ["Service GO Transit - Aucune mise à jour"]
        }