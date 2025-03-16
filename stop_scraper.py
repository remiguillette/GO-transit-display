
from datetime import datetime
import logging
from gtfs_parser import gtfs_data

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class StopScraper:
    """Scraper specifically for stop/station data with protections"""
    
    def __init__(self):
        if not gtfs_data.stations:
            gtfs_data.load_data()
            
    def clean_station_name(self, station_name):
        """Clean station name by removing unnecessary suffixes"""
        return station_name.replace(" GO", "").replace(" Station", "")
            
    def get_stops_for_route(self, line_code, direction="outbound"):
        """Get ordered stops for a specific route line"""
        key_stations = {
            'LW': ['Union Station', 'Exhibition', 'Mimico', 'Port Credit', 
                  'Oakville', 'Burlington', 'Aldershot', 'Hamilton'],
            'LE': ['Union Station', 'Danforth', 'Scarborough', 'Eglinton',
                  'Guildwood', 'Rouge Hill', 'Pickering', 'Ajax', 
                  'Whitby', 'Oshawa'],
            'ST': ['Union Station', 'Kennedy', 'Agincourt', 'Milliken',
                  'Unionville', 'Centennial', 'Markham', 'Mount Joy', 
                  'Stouffville'],
            'RH': ['Union Station', 'Old Cummer', 'Langstaff', 'Richmond Hill'],
            'BR': ['Union Station', 'Downsview Park', 'Rutherford', 'Maple',
                  'King City', 'Aurora', 'Newmarket', 'East Gwillimbury',
                  'Bradford', 'Barrie South', 'Allandale Waterfront'],
            'KI': ['Union Station', 'Bloor', 'Weston', 'Etobicoke North',
                  'Malton', 'Bramalea', 'Brampton', 'Mount Pleasant',
                  'Georgetown', 'Acton', 'Guelph Central', 'Kitchener'],
            'MI': ['Union Station', 'Kipling', 'Dixie', 'Cooksville',
                  'Erindale', 'Streetsville', 'Meadowvale', 'Lisgar', 
                  'Milton']
        }
        
        if line_code not in key_stations:
            return []
            
        stops = key_stations[line_code]
        if direction == "inbound" and len(stops) > 1:
            stops = stops[::-1]  # Reverse for inbound
            
        return stops
        
    def get_upcoming_stops(self, origin_station, destination, line_code):
        """Get list of upcoming stops between origin and destination"""
        # Clean station names for comparison
        clean_origin = self.clean_station_name(origin_station)
        clean_destination = self.clean_station_name(destination)
        
        all_stops = self.get_stops_for_route(line_code)
        all_stops_clean = [self.clean_station_name(stop) for stop in all_stops]
        
        try:
            start_idx = all_stops_clean.index(clean_origin)
            end_idx = all_stops_clean.index(clean_destination)
            
            if start_idx < end_idx:  # Outbound
                return all_stops[start_idx + 1:end_idx + 1]
            else:  # Inbound
                return all_stops[end_idx:start_idx][::-1]
        except ValueError:
            return []
            
    def format_stops_display(self, stops, max_stops=3):
        """Format stops for display, limiting to max_stops"""
        if not stops:
            return "Express Service"
            
        # Already clean names in get_stops_for_route
        display_stops = stops[:max_stops]
        return " • ".join(display_stops)

# Create an instance for importing
stop_scraper = StopScraper()
