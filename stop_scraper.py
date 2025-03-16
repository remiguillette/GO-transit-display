import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StopScraper:
    def __init__(self):
        self.base_url = "https://www.gotransit.com"
        self.routes = {
            'LW': 'Lakeshore West',
            'LE': 'Lakeshore East',
            'ST': 'Stouffville',
            'RH': 'Richmond Hill',
            'BR': 'Barrie',
            'KI': 'Kitchener',
            'MI': 'Milton'
        }

    def get_stops_for_route(self, line_code):
        """Get all stops for a given route"""
        if line_code == 'LW':
            return ['Union Station', 'Exhibition', 'Mimico', 'Long Branch', 'Port Credit', 'Clarkson', 'Oakville', 'Bronte', 'Appleby', 'Burlington', 'Aldershot', 'Hamilton']
        elif line_code == 'LE':
            return ['Union Station', 'Danforth', 'Scarborough', 'Eglinton', 'Guildwood', 'Rouge Hill', 'Pickering', 'Ajax', 'Whitby', 'Oshawa']
        elif line_code == 'ST':
            return ['Union Station', 'Kennedy', 'Agincourt', 'Milliken', 'Unionville', 'Centennial', 'Markham', 'Mount Joy', 'Stouffville']
        elif line_code == 'RH':
            return ['Union Station', 'Old Cummer', 'Langstaff', 'Richmond Hill', 'Gormley', 'Bloomington']
        elif line_code == 'BR':
            return ['Union Station', 'Downsview Park', 'Rutherford', 'Maple', 'King City', 'Aurora', 'Newmarket', 'East Gwillimbury', 'Bradford', 'Barrie South', 'Allandale Waterfront']
        elif line_code == 'KI':
            return ['Union Station', 'Bloor', 'Weston', 'Etobicoke North', 'Malton', 'Bramalea', 'Brampton', 'Mount Pleasant', 'Georgetown', 'Acton', 'Guelph Central', 'Kitchener']
        elif line_code == 'MI':
            return ['Union Station', 'Kipling', 'Dixie', 'Cooksville', 'Erindale', 'Streetsville', 'Meadowvale', 'Lisgar', 'Milton']
        return []

    def clean_station_name(self, station_name):
        """Clean station name by removing line codes"""
        return station_name.replace('(BR)', '').replace('(LW)', '').replace('(LE)', '').strip()

    def get_upcoming_stops(self, current_station, destination, line_code):
        """Get upcoming stops between current station and destination"""
        all_stops = self.get_stops_for_route(line_code)
        try:
            current_idx = all_stops.index(current_station)
            dest_idx = all_stops.index(destination)

            if current_idx < dest_idx:
                return all_stops[current_idx + 1:dest_idx + 1]
            else:
                return all_stops[dest_idx:current_idx][::-1]
        except ValueError:
            logger.error(f"Station not found: {current_station} or {destination}")
            return []

    def format_stops_display(self, stops):
        """Format stops for display"""
        if not stops:
            return ""
        return " • ".join(stops)

# Create an instance for importing
stop_scraper = StopScraper()