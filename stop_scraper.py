
import requests
import logging
import csv
import os
import random
from datetime import datetime, timedelta

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
                    route_id = row['route_id']
                    if route_id:
                        self.routes[route_id] = {
                            'name': row['route_long_name'],
                            'code': row.get('route_short_name', ''),
                            'color': row.get('route_color', '')
                        }
        except FileNotFoundError:
            logger.warning("Routes file not found, using default routes")
            self.routes = {
                'LW': {'name': 'Lakeshore West', 'code': 'LW', 'color': '00A0DF'},
                'LE': {'name': 'Lakeshore East', 'code': 'LE', 'color': '00853F'},
                'ST': {'name': 'Stouffville', 'code': 'ST', 'color': 'F5A623'},
                'RH': {'name': 'Richmond Hill', 'code': 'RH', 'color': '8DC63F'},
                'BR': {'name': 'Barrie', 'code': 'BR', 'color': '911D74'},
                'KI': {'name': 'Kitchener', 'code': 'KI', 'color': 'DA291C'},
                'MI': {'name': 'Milton', 'code': 'MI', 'color': '0052A5'}
            }

        # Load stops
        self.station_data = {}
        stops_file = os.path.join('attached_assets', 'stops.txt')
        try:
            with open(stops_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    stop_id = row['stop_id']
                    if stop_id:
                        self.station_data[stop_id] = {
                            'name': row['stop_name'],
                            'lat': float(row['stop_lat']),
                            'lon': float(row['stop_lon']),
                            'zone_id': row.get('zone_id', ''),
                            'wheelchair_boarding': int(row.get('wheelchair_boarding', 0)) == 1
                        }
        except FileNotFoundError:
            logger.warning("Stops file not found")

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

    def generate_schedule(self, station_name, num_trains=48):
        """Generate a schedule for the given station"""
        try:
            current_time = datetime.now()
            schedule = []
            
            # Get station info
            station_info = None
            for info in self.station_data.values():
                if info['name'] == station_name:
                    station_info = info
                    break

            if not station_info:
                logger.warning(f"Station info not found for {station_name}, using defaults")
                station_info = {'wheelchair_boarding': True}

            # Get all possible lines for this station
            available_lines = []
            for line_code in ['LW', 'LE', 'ST', 'RH', 'BR', 'KI', 'MI']:
                if station_name in self.get_stops_for_route(line_code):
                    available_lines.append(line_code)

            if not available_lines:
                available_lines = ['LW']  # Default to Lakeshore West
                logger.info(f"No lines found for {station_name}, defaulting to LW")

            for i in range(num_trains):
                try:
                    line_code = available_lines[i % len(available_lines)]
                    route_stops = self.get_stops_for_route(line_code)
                    
                    if not route_stops:
                        continue

                    try:
                        station_index = route_stops.index(station_name)
                    except ValueError:
                        logger.warning(f"Station {station_name} not found in route {line_code}")
                        continue

                    # Determine direction and destination
                    if i % 2 == 0:  # Outbound
                        if station_index >= len(route_stops) - 1:
                            continue
                        destination = route_stops[-1]
                    else:  # Inbound
                        if station_index == 0:
                            continue
                        destination = route_stops[0]

                    # Generate departure time
                    departure_time = current_time + timedelta(minutes=15 * i)
                    
                    # Random status generation (mostly on time)
                    status = "On time"
                    platform = str(random.randint(1, 12))
                    
                    if line_code not in self.routes:
                        logger.warning(f"Route {line_code} not found in routes data")
                        continue

                    # Create schedule entry
                    schedule.append({
                        "departure_time": departure_time,
                        "destination": destination,
                        "route_code": line_code,
                        "status": status,
                        "platform": platform,
                        "accessible": station_info.get('wheelchair_boarding', True),
                        "train_number": f"{line_code}{random.randint(100, 999)}",
                        "color": f"#{self.routes[line_code]['color']}"
                    })
                except Exception as e:
                    logger.error(f"Error generating schedule entry: {e}")
                    continue

            # Sort by departure time
            schedule.sort(key=lambda x: x["departure_time"])
            return schedule

        except Exception as e:
            logger.error(f"Error generating schedule: {e}")
            return []

        # Sort by departure time
        schedule.sort(key=lambda x: x["departure_time"])
        return schedule

# Create an instance for importing
stop_scraper = StopScraper()
