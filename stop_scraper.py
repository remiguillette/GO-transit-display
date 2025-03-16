
import requests
import logging
import csv
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StopScraper:
    def __init__(self):
        self.base_url = "https://www.gotransit.com"
        self.routes = {}
        self.load_gtfs_data()

    def load_gtfs_data(self):
        """Load route and stop data from GTFS files"""
        # Load routes
        routes_file = os.path.join('attached_assets', 'routes.txt')
        try:
            with open(routes_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    route_id = row['route_id'].split('-')[1] if '-' in row['route_id'] else row['route_id']
                    if route_id in ['LW', 'LE', 'ST', 'RH', 'BR', 'KI', 'MI']:
                        self.routes[route_id] = row['route_long_name']
        except FileNotFoundError:
            logger.warning("Routes file not found, using default routes")
            self.routes = {
                'LW': 'Lakeshore West',
                'LE': 'Lakeshore East',
                'ST': 'Stouffville',
                'RH': 'Richmond Hill',
                'BR': 'Barrie',
                'KI': 'Kitchener',
                'MI': 'Milton'
            }

        # Load stops
        self.station_data = {}
        stops_file = os.path.join('attached_assets', 'stops.txt')
        try:
            with open(stops_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.station_data[row['stop_id']] = {
                        'name': row['stop_name'],
                        'lat': float(row['stop_lat']),
                        'lon': float(row['stop_lon']),
                        'zone_id': row.get('zone_id', ''),
                        'wheelchair_boarding': int(row.get('wheelchair_boarding', 0)) == 1
                    }
        except FileNotFoundError:
            logger.warning("Stops file not found, using backup station data")

    def get_stops_for_route(self, line_code):
        """Get all stops for a given route"""
        if line_code == 'LW':
            return ['Union Station', 'Exhibition GO', 'Mimico GO', 'Long Branch GO', 'Port Credit GO', 
                   'Clarkson GO', 'Oakville GO', 'Bronte GO', 'Appleby GO', 'Burlington GO', 
                   'Aldershot GO', 'Hamilton GO', 'West Harbour GO', 'St. Catharines GO', 'Niagara Falls GO']
        elif line_code == 'LE':
            return ['Union Station', 'Danforth GO', 'Scarborough GO', 'Eglinton GO', 'Guildwood GO',
                   'Rouge Hill GO', 'Pickering GO', 'Ajax GO', 'Whitby GO', 'Oshawa GO']
        elif line_code == 'ST':
            return ['Union Station', 'Kennedy GO', 'Agincourt GO', 'Milliken GO', 'Unionville GO',
                   'Centennial GO', 'Markham GO', 'Mount Joy GO', 'Stouffville GO', 'Old Elm GO']
        elif line_code == 'RH':
            return ['Union Station', 'Old Cummer GO', 'Langstaff GO', 'Richmond Hill GO',
                   'Gormley GO', 'Bloomington GO']
        elif line_code == 'BR':
            return ['Union Station', 'Downsview Park GO', 'Rutherford GO', 'Maple GO', 'King City GO',
                   'Aurora GO', 'Newmarket GO', 'East Gwillimbury GO', 'Bradford GO', 
                   'Barrie South GO', 'Allandale Waterfront GO']
        elif line_code == 'KI':
            return ['Union Station', 'Bloor GO', 'Weston GO', 'Etobicoke North GO', 'Malton GO',
                   'Bramalea GO', 'Brampton GO', 'Mount Pleasant GO', 'Georgetown GO',
                   'Acton GO', 'Guelph Central GO', 'Kitchener GO']
        elif line_code == 'MI':
            return ['Union Station', 'Kipling GO', 'Dixie GO', 'Cooksville GO', 'Erindale GO',
                   'Streetsville GO', 'Meadowvale GO', 'Lisgar GO', 'Milton GO']
        return []

    def clean_station_name(self, station_name):
        """Clean station name by removing line codes and standardizing format"""
        name = station_name.replace('(BR)', '').replace('(LW)', '').replace('(LE)', '').strip()
        if not name.endswith(' GO') and name != 'Union Station':
            name = f"{name} GO"
        return name

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
        """Format stops for display with improved formatting"""
        if not stops:
            return ""
        return " • ".join([self.clean_station_name(stop) for stop in stops])

    def get_all_stations(self):
        """Get a list of all unique stations across all routes"""
        all_stations = set()
        for line_code in self.routes.keys():
            all_stations.update(self.get_stops_for_route(line_code))
        return sorted(list(all_stations))

    def get_station_info(self, station_name):
        """Get detailed information about a station"""
        for stop_id, info in self.station_data.items():
            if info['name'].replace(' GO', '') == station_name.replace(' GO', ''):
                return info
        return None

# Create an instance for importing
stop_scraper = StopScraper()
