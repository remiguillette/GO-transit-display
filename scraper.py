"""GO Transit schedule scraper module"""
import logging
from datetime import datetime, timedelta
import urllib.request
import json
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class GOTransitScraper:
    """Scraper for GO Transit schedules"""

    # GO Transit line codes and their colors
    LINE_COLORS = {
        'LW': '#00853F',  # Lakeshore West
        'LE': '#231F20',  # Lakeshore East
        'ST': '#F5A81C',  # Stouffville
        'RH': '#DA291C',  # Richmond Hill
        'BR': '#0079C2',  # Barrie
        'KI': '#9B2743',  # Kitchener
        'MI': '#00A4E4'   # Milton
    }

    # Stations with accessibility information
    STATIONS = {
        'Union': {
            'name': 'Union Station',
            'name_fr': 'Gare Union',
            'code': 'UN',
            'accessible': True,
            'lines': ['LW', 'LE', 'ST', 'RH', 'BR', 'KI', 'MI']
        },
        'Mimico': {
            'name': 'Mimico',
            'name_fr': 'Mimico',
            'code': 'MI',
            'accessible': True,
            'lines': ['LW']
        },
        'Exhibition': {
            'name': 'Exhibition',
            'name_fr': 'Exhibition',
            'code': 'EX',
            'accessible': True,
            'lines': ['LW']
        },
        'Bloor': {
            'name': 'Bloor',
            'name_fr': 'Bloor',
            'code': 'BL',
            'accessible': True,
            'lines': ['KI']
        },
        'Weston': {
            'name': 'Weston',
            'name_fr': 'Weston',
            'code': 'WE',
            'accessible': True,
            'lines': ['KI']
        },
        'Etobicoke North': {
            'name': 'Etobicoke North',
            'name_fr': 'Etobicoke Nord',
            'code': 'EN',
            'accessible': True,
            'lines': ['KI']
        },
        'Malton': {
            'name': 'Malton',
            'name_fr': 'Malton',
            'code': 'MA',
            'accessible': True,
            'lines': ['KI']
        }
    }

    def __init__(self):
        """Initialize the scraper"""
        self.base_url = "https://www.gotracker.ca/gotracker/web/ServiceData.aspx"

    def _get_station_info(self, station: str) -> Dict:
        """Get station information"""
        return self.STATIONS.get(station, {
            'name': station,
            'name_fr': station,
            'code': 'UN',
            'accessible': True,
            'lines': ['LW']
        })

    def _parse_time(self, time_str: str) -> datetime:
        """Parse time string to datetime object"""
        try:
            current_date = datetime.now().date()
            return datetime.strptime(f"{current_date} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError as e:
            logger.error(f"Error parsing time: {e}")
            return datetime.now()

    def get_station_schedule(self, station: str) -> List[Dict]:
        """
        Fetch schedule for a specific station
        Returns list of schedule dictionaries
        """
        try:
            station_info = self._get_station_info(station)

            # In production, implement actual API call to gotracker.ca
            # For now, generate demo data
            return self._get_demo_schedule(station, station_info)

        except Exception as e:
            logger.error(f"Error fetching schedule: {e}")
            return self._get_demo_schedule(station, station_info)

    def _get_demo_schedule(self, station: str, station_info: Dict) -> List[Dict]:
        """Generate demo schedule data"""
        current_time = datetime.now()

        # Demo schedule data with proper line codes and accessibility
        schedules = [
            {
                'train_number': 'ST01',
                'destination': 'Stouffville',
                'departure_time': current_time + timedelta(minutes=15),
                'status': 'On Time',
                'platform': '15',
                'route_code': 'ST',
                'accessible': True,
                'color': self.LINE_COLORS['ST']
            },
            {
                'train_number': 'RH02',
                'destination': 'Richmond Hill',
                'departure_time': current_time + timedelta(minutes=30),
                'status': 'DELAYED',
                'platform': None,
                'route_code': 'RH',
                'accessible': True,
                'color': self.LINE_COLORS['RH']
            },
            {
                'train_number': 'BR01',
                'destination': 'Barrie',
                'departure_time': current_time + timedelta(minutes=45),
                'status': 'CANCELLED',
                'platform': None,
                'route_code': 'BR',
                'accessible': True,
                'color': self.LINE_COLORS['BR']
            },
            {
                'train_number': 'LW01',
                'destination': 'Aldershot',
                'departure_time': current_time + timedelta(minutes=60),
                'status': 'On Time',
                'platform': '12',
                'route_code': 'LW',
                'accessible': True,
                'color': self.LINE_COLORS['LW']
            }
        ]

        return schedules

scraper = GOTransitScraper()