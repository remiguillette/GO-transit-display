import os
import csv
import logging
from datetime import datetime
from flask import current_app
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class GTFSData:
    """Class to handle GTFS data parsing and storage"""
    
    def __init__(self):
        self.routes = {}  # Routes by route_id
        self.stops = {}   # Stops by stop_id
        self.trips = {}   # Trips by trip_id
        self.agencies = {}  # Agencies by agency_id
        self.stations = {}  # Stations by stop_id (filtered for train stations)
        
        # GO Transit colors by line code
        self.LINE_COLORS = {
            "LW": "#00A0DF",  # Lakeshore West - Blue
            "LE": "#00853F",  # Lakeshore East - Green
            "ST": "#F5A623",  # Stouffville - Orange
            "RH": "#8DC63F",  # Richmond Hill - Light Green
            "BR": "#911D74",  # Barrie - Purple
            "KI": "#DA291C",  # Kitchener - Red
            "MI": "#0052A5",  # Milton - Dark Blue
            "GO": "#4D4D4D"   # Default GO Transit - Grey
        }
    
    def get_line_color(self, line_code: str) -> str:
        """Get the official GO Transit color for a line code"""
        return self.LINE_COLORS.get(line_code, self.LINE_COLORS["GO"])
    
    def load_data(self) -> None:
        """Load all GTFS data from files"""
        # Define the path to the GTFS files
        base_path = "attached_assets"
        
        # Load agencies
        self._load_agencies(os.path.join(base_path, "agency.txt"))
        
        # Load routes
        self._load_routes(os.path.join(base_path, "routes.txt"))
        
        # Load stops (stations)
        self._load_stops(os.path.join(base_path, "stops.txt"))
        
        # Load trips
        self._load_trips(os.path.join(base_path, "trips.txt"))
        
        logger.info(f"Loaded {len(self.routes)} routes, {len(self.stops)} stops, {len(self.trips)} trips, {len(self.stations)} stations")
    
    def _load_agencies(self, filepath: str) -> None:
        """Load agency data from a GTFS agency.txt file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    agency_id = row.get('agency_id', 'GO')
                    self.agencies[agency_id] = {
                        'name': row.get('agency_name', 'GO Transit'),
                        'url': row.get('agency_url', ''),
                        'timezone': row.get('agency_timezone', ''),
                        'lang': row.get('agency_lang', ''),
                        'phone': row.get('agency_phone', ''),
                        'fare_url': row.get('agency_fare_url', '')
                    }
                    
                    # If we found at least one agency, this is good enough
                    logger.info(f"Loaded agency: {agency_id}")
                    
                    # Default to GO Transit if no agencies found
                    if not self.agencies:
                        self.agencies['GO'] = {
                            'name': 'GO Transit',
                            'url': 'https://www.gotransit.com',
                            'timezone': 'America/Toronto',
                            'lang': 'en',
                            'phone': '1-888-GET-ON-GO',
                            'fare_url': 'https://www.gotransit.com'
                        }
                    
        except FileNotFoundError:
            logger.warning(f"Agency file not found: {filepath}")
            # Default to GO Transit if file not found
            self.agencies['GO'] = {
                'name': 'GO Transit',
                'url': 'https://www.gotransit.com',
                'timezone': 'America/Toronto',
                'lang': 'en',
                'phone': '1-888-GET-ON-GO',
                'fare_url': 'https://www.gotransit.com'
            }
        except Exception as e:
            logger.error(f"Error loading agency data: {e}")
    
    def _load_routes(self, filepath: str) -> None:
        """Load route data from a GTFS routes.txt file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Skip rows without route_id
                    if 'route_id' not in row:
                        continue
                    
                    # Extract the route ID
                    route_id = row['route_id']
                    
                    # Get the route short name (e.g., "LW")
                    route_short_name = row.get('route_short_name', '')
                    
                    # Extract the route code (e.g., "LW" from "Lakeshore West")
                    route_name = row.get('route_long_name', '')
                    route_code = route_short_name if route_short_name else self._extract_route_code(route_name)
                    
                    # Add to routes dictionary
                    self.routes[route_id] = {
                        'short_name': route_short_name,
                        'long_name': route_name,
                        'route_code': route_code,
                        'agency_id': row.get('agency_id', ''),
                        'type': int(row.get('route_type', 0)),
                        'color': '#' + row.get('route_color', 'FFFFFF'),
                        'text_color': '#' + row.get('route_text_color', '000000')
                    }
                
                logger.info(f"Loaded {len(self.routes)} routes")
                
                # If no routes were loaded, add default routes
                if not self.routes:
                    default_routes = [
                        ('LW', 'LW', 'Lakeshore West', '00A0DF'),
                        ('LE', 'LE', 'Lakeshore East', '00853F'),
                        ('ST', 'ST', 'Stouffville', 'F5A623'),
                        ('RH', 'RH', 'Richmond Hill', '8DC63F'),
                        ('BR', 'BR', 'Barrie', '911D74'),
                        ('KI', 'KI', 'Kitchener', 'DA291C'),
                        ('MI', 'MI', 'Milton', '0052A5')
                    ]
                    
                    for route_id, short_name, long_name, color in default_routes:
                        self.routes[route_id] = {
                            'short_name': short_name,
                            'long_name': long_name,
                            'route_code': short_name,
                            'agency_id': 'GO',
                            'type': 2,  # Rail
                            'color': f'#{color}',
                            'text_color': '#FFFFFF'
                        }
                    
                    logger.info(f"Added {len(default_routes)} default routes")
                    
        except FileNotFoundError:
            logger.warning(f"Routes file not found: {filepath}")
            # Add default routes
            default_routes = [
                ('LW', 'LW', 'Lakeshore West', '00A0DF'),
                ('LE', 'LE', 'Lakeshore East', '00853F'),
                ('ST', 'ST', 'Stouffville', 'F5A623'),
                ('RH', 'RH', 'Richmond Hill', '8DC63F'),
                ('BR', 'BR', 'Barrie', '911D74'),
                ('KI', 'KI', 'Kitchener', 'DA291C'),
                ('MI', 'MI', 'Milton', '0052A5')
            ]
            
            for route_id, short_name, long_name, color in default_routes:
                self.routes[route_id] = {
                    'short_name': short_name,
                    'long_name': long_name,
                    'route_code': short_name,
                    'agency_id': 'GO',
                    'type': 2,  # Rail
                    'color': f'#{color}',
                    'text_color': '#FFFFFF'
                }
            
            logger.info(f"Added {len(default_routes)} default routes")
            
        except Exception as e:
            logger.error(f"Error loading route data: {e}")
    
    def _load_stops(self, filepath: str) -> None:
        """Load stop data from a GTFS stops.txt file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Skip rows without stop_id
                    if 'stop_id' not in row:
                        continue
                        
                    stop_id = row['stop_id']
                    stop_name = row.get('stop_name', f"Stop {stop_id}")
                    
                    # Add to stops dictionary
                    self.stops[stop_id] = {
                        'name': stop_name,
                        'lat': float(row.get('stop_lat', 0)),
                        'lon': float(row.get('stop_lon', 0)),
                        'code': row.get('stop_code', ''),
                        'desc': row.get('stop_desc', ''),
                        'location_type': int(row.get('location_type', 0)),
                        'parent_station': row.get('parent_station', ''),
                        'wheelchair_boarding': int(row.get('wheelchair_boarding', 0))
                    }
                    
                    # All GO stops are stations for our purposes
                    # In GO data, they're coded as location_type=0
                    # We'll append " GO" if it's not already in the name
                    if not stop_name.endswith(" GO") and not stop_name.endswith(" Station"):
                        station_name = f"{stop_name} GO"
                    else:
                        station_name = stop_name
                        
                    self.stations[stop_id] = {
                        'name': station_name,
                        'lat': float(row.get('stop_lat', 0)),
                        'lon': float(row.get('stop_lon', 0)),
                        'code': stop_id,
                        'accessible': int(row.get('wheelchair_boarding', 0)) > 0,
                        'lines': [],  # Will be populated as we process trips
                    }
                
                logger.info(f"Loaded {len(self.stops)} stops and {len(self.stations)} stations")
                
                # If no stations were loaded, add default stations
                if not self.stations:
                    default_stations = [
                        # Lakeshore West
                        ('UN', 'Union Station', 43.645195, -79.3806, ['LW', 'LE', 'ST', 'RH', 'BR', 'KI', 'MI']),
                        ('EX', 'Exhibition GO', 43.6346, -79.4153, ['LW']),
                        ('MI', 'Mimico GO', 43.6211, -79.4954, ['LW']),
                        ('LO', 'Long Branch GO', 43.5950, -79.5408, ['LW']),
                        ('PO', 'Port Credit GO', 43.5572, -79.5858, ['LW']),
                        ('CL', 'Clarkson GO', 43.5110, -79.6347, ['LW']),
                        ('OA', 'Oakville GO', 43.4561, -79.6832, ['LW']),
                        ('BV', 'Bronte GO', 43.3944, -79.7562, ['LW']),
                        ('AP', 'Appleby GO', 43.3819, -79.8019, ['LW']),
                        ('BU', 'Burlington GO', 43.3386, -79.8027, ['LW']),
                        ('AL', 'Aldershot GO', 43.3165, -79.8342, ['LW']),
                        ('HA', 'Hamilton GO', 43.2543, -79.8813, ['LW']),
                        ('WH', 'West Harbour GO', 43.2690, -79.8740, ['LW']),
                        ('ST', 'St. Catharines GO', 43.1593, -79.2342, ['LW']),
                        ('NF', 'Niagara Falls GO', 43.1088, -79.0632, ['LW']),
                        
                        # Lakeshore East
                        ('DA', 'Danforth GO', 43.6883, -79.3262, ['LE']),
                        ('SC', 'Scarborough GO', 43.7071, -79.2580, ['LE']),
                        ('EG', 'Eglinton GO', 43.7256, -79.2262, ['LE']),
                        ('GU', 'Guildwood GO', 43.7637, -79.1908, ['LE']),
                        ('RO', 'Rouge Hill GO', 43.8012, -79.1510, ['LE']),
                        ('PI', 'Pickering GO', 43.8342, -79.0887, ['LE']),
                        ('AJ', 'Ajax GO', 43.8511, -79.0319, ['LE']),
                        ('WH', 'Whitby GO', 43.8669, -78.9362, ['LE']),
                        ('OS', 'Oshawa GO', 43.8789, -78.8990, ['LE']),
                        
                        # Stouffville
                        ('KE', 'Kennedy GO', 43.7732, -79.2683, ['ST']),
                        ('AG', 'Agincourt GO', 43.7835, -79.2839, ['ST']),
                        ('ML', 'Milliken GO', 43.8276, -79.2984, ['ST']),
                        ('UV', 'Unionville GO', 43.8543, -79.3131, ['ST']),
                        ('CE', 'Centennial GO', 43.8767, -79.3132, ['ST']),
                        ('MK', 'Markham GO', 43.8910, -79.2539, ['ST']),
                        ('MJ', 'Mount Joy GO', 43.9143, -79.2590, ['ST']),
                        ('SV', 'Stouffville GO', 43.9696, -79.3210, ['ST']),
                        ('LI', 'Lincolnville GO', 44.0064, -79.1943, ['ST']),
                        
                        # Richmond Hill
                        ('OC', 'Old Cummer GO', 43.7841, -79.3604, ['RH']),
                        ('LA', 'Langstaff GO', 43.8121, -79.4084, ['RH']),
                        ('RM', 'Richmond Hill GO', 43.8713, -79.4252, ['RH']),
                        ('GO', 'Gormley GO', 43.9334, -79.3836, ['RH']),
                        ('BL', 'Bloomington GO', 44.0004, -79.4150, ['RH']),
                        
                        # Barrie
                        ('DW', 'Downsview Park GO', 43.7537, -79.4790, ['BR']),
                        ('RD', 'Rutherford GO', 43.8371, -79.4980, ['BR']),
                        ('MP', 'Maple GO', 43.8598, -79.5137, ['BR']),
                        ('KI', 'King City GO', 43.9271, -79.5246, ['BR']),
                        ('AU', 'Aurora GO', 43.9924, -79.4621, ['BR']),
                        ('NE', 'Newmarket GO', 44.0510, -79.4611, ['BR']),
                        ('EA', 'East Gwillimbury GO', 44.0813, -79.4622, ['BR']),
                        ('BD', 'Bradford GO', 44.1206, -79.5612, ['BR']),
                        ('BA', 'Barrie South GO', 44.3228, -79.6883, ['BR']),
                        ('AC', 'Allandale Waterfront GO', 44.3854, -79.6883, ['BR']),
                        
                        # Kitchener
                        ('WE', 'Weston GO', 43.7066, -79.5238, ['KI']),
                        ('EP', 'Etobicoke North GO', 43.7064, -79.5546, ['KI']),
                        ('MA', 'Malton GO', 43.7078, -79.6100, ['KI']),
                        ('BP', 'Bramalea GO', 43.7234, -79.6882, ['KI']),
                        ('BM', 'Brampton GO', 43.6828, -79.7560, ['KI']),
                        ('MO', 'Mount Pleasant GO', 43.6881, -79.8046, ['KI']),
                        ('GT', 'Georgetown GO', 43.6563, -79.9288, ['KI']),
                        ('AC', 'Acton GO', 43.6368, -80.0321, ['KI']),
                        ('GU', 'Guelph Central GO', 43.5448, -80.2461, ['KI']),
                        ('KT', 'Kitchener GO', 43.4537, -80.4976, ['KI']),
                        
                        # Milton
                        ('KP', 'Kipling GO', 43.6376, -79.5360, ['MI']),
                        ('DI', 'Dixie GO', 43.6285, -79.5872, ['MI']),
                        ('CO', 'Cooksville GO', 43.5893, -79.6216, ['MI']),
                        ('ER', 'Erindale GO', 43.5643, -79.6599, ['MI']),
                        ('SG', 'Streetsville GO', 43.5884, -79.7146, ['MI']),
                        ('ME', 'Meadowvale GO', 43.6111, -79.7574, ['MI']),
                        ('LI', 'Lisgar GO', 43.5980, -79.8005, ['MI']),
                        ('MT', 'Milton GO', 43.5177, -79.8637, ['MI'])
                    ]
                    
                    for code, name, lat, lon, lines in default_stations:
                        self.stations[code] = {
                            'name': name,
                            'lat': lat,
                            'lon': lon,
                            'code': code,
                            'accessible': True,
                            'lines': lines
                        }
                    
                    logger.info(f"Added {len(default_stations)} default stations")
                    
        except FileNotFoundError:
            logger.warning(f"Stops file not found: {filepath}")
            # Add default stations - use the same extensive list as above
            default_stations = [
                # Lakeshore West
                ('UN', 'Union Station', 43.645195, -79.3806, ['LW', 'LE', 'ST', 'RH', 'BR', 'KI', 'MI']),
                ('EX', 'Exhibition GO', 43.6346, -79.4153, ['LW']),
                ('MI', 'Mimico GO', 43.6211, -79.4954, ['LW']),
                ('LO', 'Long Branch GO', 43.5950, -79.5408, ['LW']),
                ('PO', 'Port Credit GO', 43.5572, -79.5858, ['LW']),
                ('CL', 'Clarkson GO', 43.5110, -79.6347, ['LW']),
                ('OA', 'Oakville GO', 43.4561, -79.6832, ['LW']),
                ('BV', 'Bronte GO', 43.3944, -79.7562, ['LW']),
                ('AP', 'Appleby GO', 43.3819, -79.8019, ['LW']),
                ('BU', 'Burlington GO', 43.3386, -79.8027, ['LW']),
                ('AL', 'Aldershot GO', 43.3165, -79.8342, ['LW']),
                ('HA', 'Hamilton GO', 43.2543, -79.8813, ['LW']),
                ('WH', 'West Harbour GO', 43.2690, -79.8740, ['LW']),
                ('ST', 'St. Catharines GO', 43.1593, -79.2342, ['LW']),
                ('NF', 'Niagara Falls GO', 43.1088, -79.0632, ['LW']),
                
                # Lakeshore East
                ('DA', 'Danforth GO', 43.6883, -79.3262, ['LE']),
                ('SC', 'Scarborough GO', 43.7071, -79.2580, ['LE']),
                ('EG', 'Eglinton GO', 43.7256, -79.2262, ['LE']),
                ('GU', 'Guildwood GO', 43.7637, -79.1908, ['LE']),
                ('RO', 'Rouge Hill GO', 43.8012, -79.1510, ['LE']),
                ('PI', 'Pickering GO', 43.8342, -79.0887, ['LE']),
                ('AJ', 'Ajax GO', 43.8511, -79.0319, ['LE']),
                ('WH', 'Whitby GO', 43.8669, -78.9362, ['LE']),
                ('OS', 'Oshawa GO', 43.8789, -78.8990, ['LE']),
                
                # Stouffville
                ('KE', 'Kennedy GO', 43.7732, -79.2683, ['ST']),
                ('AG', 'Agincourt GO', 43.7835, -79.2839, ['ST']),
                ('ML', 'Milliken GO', 43.8276, -79.2984, ['ST']),
                ('UV', 'Unionville GO', 43.8543, -79.3131, ['ST']),
                ('CE', 'Centennial GO', 43.8767, -79.3132, ['ST']),
                ('MK', 'Markham GO', 43.8910, -79.2539, ['ST']),
                ('MJ', 'Mount Joy GO', 43.9143, -79.2590, ['ST']),
                ('SV', 'Stouffville GO', 43.9696, -79.3210, ['ST']),
                ('LI', 'Lincolnville GO', 44.0064, -79.1943, ['ST']),
                
                # Richmond Hill
                ('OC', 'Old Cummer GO', 43.7841, -79.3604, ['RH']),
                ('LA', 'Langstaff GO', 43.8121, -79.4084, ['RH']),
                ('RM', 'Richmond Hill GO', 43.8713, -79.4252, ['RH']),
                ('GO', 'Gormley GO', 43.9334, -79.3836, ['RH']),
                ('BL', 'Bloomington GO', 44.0004, -79.4150, ['RH']),
                
                # Barrie
                ('DW', 'Downsview Park GO', 43.7537, -79.4790, ['BR']),
                ('RD', 'Rutherford GO', 43.8371, -79.4980, ['BR']),
                ('MP', 'Maple GO', 43.8598, -79.5137, ['BR']),
                ('KI', 'King City GO', 43.9271, -79.5246, ['BR']),
                ('AU', 'Aurora GO', 43.9924, -79.4621, ['BR']),
                ('NE', 'Newmarket GO', 44.0510, -79.4611, ['BR']),
                ('EA', 'East Gwillimbury GO', 44.0813, -79.4622, ['BR']),
                ('BD', 'Bradford GO', 44.1206, -79.5612, ['BR']),
                ('BA', 'Barrie South GO', 44.3228, -79.6883, ['BR']),
                ('AC', 'Allandale Waterfront GO', 44.3854, -79.6883, ['BR']),
                
                # Kitchener
                ('WE', 'Weston GO', 43.7066, -79.5238, ['KI']),
                ('EP', 'Etobicoke North GO', 43.7064, -79.5546, ['KI']),
                ('MA', 'Malton GO', 43.7078, -79.6100, ['KI']),
                ('BP', 'Bramalea GO', 43.7234, -79.6882, ['KI']),
                ('BM', 'Brampton GO', 43.6828, -79.7560, ['KI']),
                ('MO', 'Mount Pleasant GO', 43.6881, -79.8046, ['KI']),
                ('GT', 'Georgetown GO', 43.6563, -79.9288, ['KI']),
                ('AC', 'Acton GO', 43.6368, -80.0321, ['KI']),
                ('GU', 'Guelph Central GO', 43.5448, -80.2461, ['KI']),
                ('KT', 'Kitchener GO', 43.4537, -80.4976, ['KI']),
                
                # Milton
                ('KP', 'Kipling GO', 43.6376, -79.5360, ['MI']),
                ('DI', 'Dixie GO', 43.6285, -79.5872, ['MI']),
                ('CO', 'Cooksville GO', 43.5893, -79.6216, ['MI']),
                ('ER', 'Erindale GO', 43.5643, -79.6599, ['MI']),
                ('SG', 'Streetsville GO', 43.5884, -79.7146, ['MI']),
                ('ME', 'Meadowvale GO', 43.6111, -79.7574, ['MI']),
                ('LI', 'Lisgar GO', 43.5980, -79.8005, ['MI']),
                ('MT', 'Milton GO', 43.5177, -79.8637, ['MI'])
            ]
            
            for code, name, lat, lon, lines in default_stations:
                self.stations[code] = {
                    'name': name,
                    'lat': lat,
                    'lon': lon,
                    'code': code,
                    'accessible': True,
                    'lines': lines
                }
            
            logger.info(f"Added {len(default_stations)} default stations")
            
        except Exception as e:
            logger.error(f"Error loading stop data: {e}")
    
    def _load_trips(self, filepath: str) -> None:
        """Load trip data from a GTFS trips.txt file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Skip rows without trip_id
                    if 'trip_id' not in row:
                        continue
                    
                    trip_id = row['trip_id']
                    
                    # Get the route for this trip
                    route_id = row.get('route_id', '')
                    route = self.routes.get(route_id, {})
                    route_code = route.get('route_code', self._extract_route_code_from_trip_id(route_id))
                    
                    # Extract train line from trip headsign if available
                    trip_headsign = row.get('trip_headsign', '')
                    if not route_code or route_code == 'GO':
                        route_code = self._extract_route_code_from_headsign(trip_headsign)
                    
                    # Add to trips dictionary
                    self.trips[trip_id] = {
                        'route_id': route_id,
                        'service_id': row.get('service_id', ''),
                        'trip_headsign': trip_headsign,
                        'direction_id': int(row.get('direction_id', 0)),
                        'block_id': row.get('block_id', ''),
                        'shape_id': row.get('shape_id', ''),
                        'wheelchair_accessible': int(row.get('wheelchair_accessible', 0)),
                        'bikes_allowed': int(row.get('bikes_allowed', 0)),
                        'route_code': route_code
                    }
                    
                    # Add line to stations that this trip serves
                    # We use this to determine which lines serve which stations
                    if route_code != 'GO':
                        for station_id in self.stations:
                            if station_id in trip_headsign or station_id.lower() in trip_headsign.lower():
                                if route_code not in self.stations[station_id].get('lines', []):
                                    if 'lines' not in self.stations[station_id]:
                                        self.stations[station_id]['lines'] = []
                                    self.stations[station_id]['lines'].append(route_code)
                
                logger.info(f"Loaded {len(self.trips)} trips")
                
                # Ensure all stations have at least one line
                for station_id, station in self.stations.items():
                    if not station.get('lines'):
                        station['lines'] = ['LW']  # Default to Lakeshore West
                    
        except FileNotFoundError:
            logger.warning(f"Trips file not found: {filepath}")
        except Exception as e:
            logger.error(f"Error loading trip data: {e}")
            
    def _extract_route_code_from_trip_id(self, route_id: str) -> str:
        """Extract line code from route ID (e.g., '01250425-LW' -> 'LW')"""
        if route_id and '-' in route_id:
            code = route_id.split('-')[-1]
            if code in ['LW', 'LE', 'ST', 'RH', 'BR', 'KI', 'MI']:
                return code
        return 'GO'
        
    def _extract_route_code_from_headsign(self, headsign: str) -> str:
        """Extract line code from trip headsign"""
        if not headsign:
            return 'GO'
            
        # First try to extract code from line mentioned in headsign
        lower_headsign = headsign.lower()
        if "lakeshore west" in lower_headsign:
            return "LW"
        elif "lakeshore east" in lower_headsign:
            return "LE"
        elif "stouffville" in lower_headsign:
            return "ST"
        elif "richmond hill" in lower_headsign:
            return "RH"
        elif "barrie" in lower_headsign:
            return "BR"
        elif "kitchener" in lower_headsign:
            return "KI"
        elif "milton" in lower_headsign:
            return "MI"
            
        # If no line mentioned, try to extract from destination
        # Many of these are specific to GO Transit network
        if "hamilton" in lower_headsign or "aldershot" in lower_headsign or "burlington" in lower_headsign:
            return "LW"
        elif "oshawa" in lower_headsign or "pickering" in lower_headsign or "ajax" in lower_headsign:
            return "LE"
        elif "lincolnville" in lower_headsign or "unionville" in lower_headsign:
            return "ST"
        elif "barrie" in lower_headsign or "aurora" in lower_headsign:
            return "BR"
        elif "richmond hill" in lower_headsign:
            return "RH"
        elif "kitchener" in lower_headsign or "bramalea" in lower_headsign:
            return "KI"
        elif "milton" in lower_headsign:
            return "MI"
            
        # Default to GO if no match
        return "GO"
    
    def _extract_route_code(self, route_name: str) -> str:
        """
        Extract the GO Transit line code from a route name.
        Example: "Lakeshore West" -> "LW"
        """
        # Map of known GO Transit lines
        line_mappings = {
            "Lakeshore West": "LW",
            "Lakeshore East": "LE",
            "Stouffville": "ST",
            "Richmond Hill": "RH",
            "Barrie": "BR",
            "Kitchener": "KI",
            "Milton": "MI"
        }
        
        # Check if the route name matches any known line
        for line_name, code in line_mappings.items():
            if line_name.lower() in route_name.lower():
                return code
        
        # Default to "GO" if no match found
        return "GO"
    
    def get_station_names(self) -> List[str]:
        """Get a list of all station names"""
        return [station['name'] for station in self.stations.values()]
    
    def get_station_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get station data by name"""
        for station_id, station in self.stations.items():
            if station['name'] == name:
                return station
        return None
    
    def get_stops_for_station(self, station_id: str) -> List[Dict[str, Any]]:
        """Get all stops associated with a station"""
        stops_list = []
        for stop_id, stop in self.stops.items():
            if stop.get('parent_station') == station_id:
                stops_list.append(stop)
        return stops_list
        
    def get_terminals(self, line_code: str) -> List[str]:
        """Get terminal stations for a line"""
        if line_code == 'LW':
            return ['Union Station', 'Niagara Falls GO']
        elif line_code == 'LE':
            return ['Union Station', 'Oshawa GO']
        elif line_code == 'ST':
            return ['Union Station', 'Lincolnville GO']
        elif line_code == 'RH':
            return ['Union Station', 'Bloomington GO']
        elif line_code == 'BR':
            return ['Union Station', 'Allandale Waterfront GO']
        elif line_code == 'KI':
            return ['Union Station', 'Kitchener GO']
        elif line_code == 'MI':
            return ['Union Station', 'Milton GO']
        return ['Union Station']

# Create a singleton instance
gtfs_data = GTFSData()