
from datetime import datetime
import logging
from gtfs_parser import gtfs_data

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class StopScraper:
    """Scraper specifically for stop/station data"""
    
    def __init__(self):
        if not gtfs_data.stations:
            gtfs_data.load_data()
            
    def get_stops_for_route(self, line_code, direction="outbound"):
        """Get ordered stops for a specific route line"""
        key_stations = {
            'LW': ['Union Station', 'Exhibition GO', 'Mimico GO', 'Port Credit GO', 
                  'Oakville GO', 'Burlington GO', 'Aldershot GO', 'Hamilton GO'],
            'LE': ['Union Station', 'Danforth GO', 'Scarborough GO', 'Eglinton GO',
                  'Guildwood GO', 'Rouge Hill GO', 'Pickering GO', 'Ajax GO', 
                  'Whitby GO', 'Oshawa GO'],
            'ST': ['Union Station', 'Kennedy GO', 'Agincourt GO', 'Milliken GO',
                  'Unionville GO', 'Centennial GO', 'Markham GO', 'Mount Joy GO', 
                  'Stouffville GO'],
            'RH': ['Union Station', 'Old Cummer GO', 'Langstaff GO', 'Richmond Hill GO'],
            'BR': ['Union Station', 'Downsview Park GO', 'Rutherford GO', 'Maple GO',
                  'King City GO', 'Aurora GO', 'Newmarket GO', 'East Gwillimbury GO',
                  'Bradford GO', 'Barrie South GO', 'Allandale Waterfront GO'],
            'KI': ['Union Station', 'Bloor GO', 'Weston GO', 'Etobicoke North GO',
                  'Malton GO', 'Bramalea GO', 'Brampton GO', 'Mount Pleasant GO',
                  'Georgetown GO', 'Acton GO', 'Guelph Central GO', 'Kitchener GO'],
            'MI': ['Union Station', 'Kipling GO', 'Dixie GO', 'Cooksville GO',
                  'Erindale GO', 'Streetsville GO', 'Meadowvale GO', 'Lisgar GO', 
                  'Milton GO']
        }
        
        if line_code not in key_stations:
            return []
            
        stops = key_stations[line_code]
        if direction == "inbound" and len(stops) > 1:
            stops = stops[::-1]  # Reverse for inbound
            
        return stops
        
    def get_upcoming_stops(self, origin_station, destination, line_code):
        """Get list of upcoming stops between origin and destination"""
        all_stops = self.get_stops_for_route(line_code)
        try:
            start_idx = all_stops.index(origin_station)
            end_idx = all_stops.index(destination)
            
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
            
        display_stops = [stop.replace(" GO", "").replace(" Station", "") 
                        for stop in stops[:max_stops]]
        return " • ".join(display_stops)

# Create an instance for importing
stop_scraper = StopScraper()
