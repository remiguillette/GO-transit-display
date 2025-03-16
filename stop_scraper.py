
import requests
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class StopScraper:
    """Class to handle GO Transit stop data and real-time information"""
    
    def __init__(self):
        self.base_url = "https://www.gotracker.ca/gotracker/web/ServiceData"
        self.routes_cache = {}
        self.stops_cache = {}
    
    def get_stops_for_route(self, route_code: str) -> List[str]:
        """Get all stops for a given route"""
        if route_code in self.routes_cache:
            return self.routes_cache[route_code]
            
        # Default stops for each line if API fails
        default_stops = {
            'LW': ['Union Station', 'Exhibition GO', 'Mimico GO', 'Long Branch GO', 'Port Credit GO', 'Clarkson GO', 
                   'Oakville GO', 'Bronte GO', 'Appleby GO', 'Burlington GO', 'Aldershot GO', 'Hamilton GO'],
            'LE': ['Union Station', 'Danforth GO', 'Scarborough GO', 'Eglinton GO', 'Guildwood GO', 'Rouge Hill GO', 
                   'Pickering GO', 'Ajax GO', 'Whitby GO', 'Oshawa GO'],
            'ST': ['Union Station', 'Kennedy GO', 'Agincourt GO', 'Milliken GO', 'Unionville GO', 'Centennial GO', 
                   'Markham GO', 'Mount Joy GO', 'Stouffville GO', 'Lincolnville GO'],
            'RH': ['Union Station', 'Old Cummer GO', 'Langstaff GO', 'Richmond Hill GO', 'Gormley GO', 'Bloomington GO'],
            'BR': ['Union Station', 'Downsview Park GO', 'Rutherford GO', 'Maple GO', 'King City GO', 'Aurora GO', 
                   'Newmarket GO', 'East Gwillimbury GO', 'Bradford GO', 'Barrie South GO', 'Allandale Waterfront GO'],
            'KI': ['Union Station', 'Bloor GO', 'Weston GO', 'Etobicoke North GO', 'Malton GO', 'Bramalea GO', 
                   'Brampton GO', 'Mount Pleasant GO', 'Georgetown GO', 'Acton GO', 'Guelph Central GO', 'Kitchener GO'],
            'MI': ['Union Station', 'Kipling GO', 'Dixie GO', 'Cooksville GO', 'Erindale GO', 'Streetsville GO', 
                   'Meadowvale GO', 'Lisgar GO', 'Milton GO']
        }
        
        try:
            # Try to get real-time data
            params = {'route': route_code}
            response = requests.get(f"{self.base_url}/GetStops", params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                stops = [stop['name'] for stop in data['stops']]
                self.routes_cache[route_code] = stops
                return stops
        except Exception as e:
            logger.warning(f"Failed to get real-time stops for route {route_code}: {e}")
        
        # Fall back to default stops
        return default_stops.get(route_code, ['Union Station'])
    
    def get_upcoming_stops(self, current_station: str, destination: str, route_code: str) -> List[str]:
        """Get upcoming stops between current station and destination"""
        all_stops = self.get_stops_for_route(route_code)
        
        try:
            current_idx = all_stops.index(current_station)
            dest_idx = all_stops.index(destination)
            
            # Handle direction
            if current_idx < dest_idx:  # Outbound
                return all_stops[current_idx + 1:dest_idx + 1]
            else:  # Inbound
                return all_stops[dest_idx:current_idx][::-1]
        except ValueError:
            return []
            
    def format_stops_display(self, stops: List[str]) -> str:
        """Format stops for display with bullet points"""
        if not stops:
            return "No stops"
            
        # Format stops with bullet points, max 3 stops
        displayed_stops = stops[:3]
        formatted = " • ".join(displayed_stops)
        
        if len(stops) > 3:
            formatted += " ..."
            
        return formatted
    
    def clean_station_name(self, station_name: str) -> str:
        """Clean up station name for display"""
        # Remove GO suffix if present
        if station_name.endswith(" GO"):
            station_name = station_name[:-3]
        # Remove additional identifiers
        station_name = station_name.replace(" Station", "")
        return station_name.strip()
    
    def get_real_time_status(self, route_code: str, train_number: str) -> Dict:
        """Get real-time status for a specific train"""
        try:
            params = {
                'route': route_code,
                'train': train_number
            }
            response = requests.get(f"{self.base_url}/GetTrainStatus", params=params, timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.warning(f"Failed to get real-time status: {e}")
        
        return {}

# Create a singleton instance
stop_scraper = StopScraper()
