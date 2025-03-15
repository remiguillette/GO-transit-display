from datetime import datetime, timedelta
import random
import logging


# Line colors based on GO Transit branding
LINE_COLORS = {
    "LW": "#00A0DF",  # Lakeshore West - Blue
    "LE": "#00853F",  # Lakeshore East - Green
    "ST": "#F5A623",  # Stouffville - Orange
    "RH": "#8DC63F",  # Richmond Hill - Light Green
    "BR": "#911D74",  # Barrie - Purple
    "KI": "#DA291C",  # Kitchener - Red
    "MI": "#0052A5",  # Milton - Dark Blue
    "GO": "#4D4D4D"   # Default GO Transit - Grey
}


# Station list with proper capitalization
STATIONS = [
    "Union", 
    "Mimico", 
    "Exhibition", 
    "Port Credit", 
    "Clarkson", 
    "Oakville",
    "Bronte",
    "Appleby",
    "Burlington",
    "Aldershot",
    "Hamilton",
    "West Harbour",
    "St. Catharines",
    "Niagara Falls",
    "Guildwood",
    "Eglinton",
    "Scarborough",
    "Rouge Hill",
    "Pickering",
    "Ajax",
    "Whitby",
    "Oshawa",
    "Barrie",
    "Bradford",
    "East Gwillimbury",
    "Newmarket",
    "Aurora",
    "King City",
    "Maple",
    "Rutherford",
    "Langstaff",
    "Richmond Hill",
    "Old Cummer",
    "Oriole",
    "Georgetown",
    "Mount Pleasant",
    "Brampton",
    "Bramalea",
    "Malton",
    "Etobicoke North",
    "Weston",
    "Bloor",
    "Kipling",
    "Dixie",
    "Cooksville"
]


# Bilingual station names (English to French)
STATION_FR = {
    "Union": "Union",
    "Mimico": "Mimico",
    "Exhibition": "Exposition",
    "Port Credit": "Port Credit",
    "Clarkson": "Clarkson",
    "Oakville": "Oakville",
    "Burlington": "Burlington",
    "Hamilton": "Hamilton",
    "West Harbour": "West Harbour",
    "St. Catharines": "St. Catharines",
    "Niagara Falls": "Chutes Niagara",
    "Guildwood": "Guildwood",
    "Scarborough": "Scarborough",
    "Pickering": "Pickering",
    "Ajax": "Ajax",
    "Whitby": "Whitby",
    "Oshawa": "Oshawa",
    "Barrie": "Barrie",
    "Newmarket": "Newmarket",
    "Aurora": "Aurora",
    "Richmond Hill": "Richmond Hill",
    "Georgetown": "Georgetown",
    "Brampton": "Brampton",
    "Malton": "Malton",
    "Weston": "Weston",
    "Bloor": "Bloor",
    "Kipling": "Kipling"
}


# Line destinations
LINE_DESTINATIONS = {
    "LW": ["Hamilton", "Aldershot", "West Harbour", "Niagara Falls"],
    "LE": ["Oshawa"],
    "ST": ["Lincolnville", "Mount Joy", "Unionville"],
    "RH": ["Richmond Hill"],
    "BR": ["Barrie", "Aurora", "Bradford"],
    "KI": ["Kitchener", "Bramalea", "Mount Pleasant", "Georgetown"],
    "MI": ["Milton"]
}


# Status options
STATUS_OPTIONS = ["On time", "Delayed", "Cancelled"]
STATUS_WEIGHTS = [0.85, 0.10, 0.05]  # Probabilities for each status


def get_line_color(line_code):
    """Get the official GO Transit color for a line code"""
    return LINE_COLORS.get(line_code, LINE_COLORS["GO"])


def get_available_stations():
    """Return the list of available stations"""
    return STATIONS


def generate_demo_schedule(station, num_trains=12):
    """
    Generate a realistic demo train schedule for a given station
    
    Args:
        station (str): Station name
        num_trains (int): Number of trains to generate
        
    Returns:
        list: List of train schedule dictionaries
    """
    logging.debug(f"Generating demo schedule for {station}")
    
    # Initialize schedule
    schedule = []
    
    # Current time for reference
    now = datetime.now()
    
    # Determine which lines serve this station
    if station == "Union":
        # Union is served by all lines
        available_lines = list(LINE_COLORS.keys())
        available_lines.remove("GO")  # Remove generic GO line
    else:
        # Simulate realistic line assignments based on station location
        # This is a simplified model
        if station in ["Mimico", "Exhibition", "Port Credit", "Clarkson", "Oakville", "Burlington", "Hamilton"]:
            available_lines = ["LW"]
        elif station in ["Guildwood", "Scarborough", "Pickering", "Ajax", "Whitby", "Oshawa"]:
            available_lines = ["LE"]
        elif station in ["Barrie", "Bradford", "Newmarket", "Aurora"]:
            available_lines = ["BR"]
        elif station in ["Richmond Hill"]:
            available_lines = ["RH"]
        elif station in ["Georgetown", "Brampton", "Malton", "Weston"]:
            available_lines = ["KI"]
        else:
            # Default to a mix of lines
            available_lines = ["LW", "LE", "BR", "KI", "MI"]
    
    # Filter to unique lines
    available_lines = list(set(available_lines))
    
    # Time interval between trains (minutes)
    interval = 15
    
    # Generate schedule entries
    for i in range(num_trains):
        # Generate departure time 
        departure_time = now + timedelta(minutes=interval * i)
        time_str = departure_time.strftime("%H:%M")
        
        # Select a random line for this train
        line_code = random.choice(available_lines)
        
        # Determine destination based on line
        if station == "Union":
            # Outbound from Union
            if line_code in LINE_DESTINATIONS:
                destination = random.choice(LINE_DESTINATIONS[line_code])
            else:
                destination = random.choice(STATIONS)
        else:
            # Inbound to Union
            destination = "Union"
        
        # Randomly assign train status based on weights
        status = random.choices(STATUS_OPTIONS, STATUS_WEIGHTS)[0]
        
        # Calculate delay if applicable
        delay_minutes = 0
        if status == "Delayed":
            delay_minutes = random.randint(5, 30)
        
        # Randomly assign platform
        platform = f"{random.randint(1, 12)}"
        
        # Randomly assign accessibility
        is_accessible = random.random() > 0.15  # 85% platforms are accessible
        
        # Generate train number
        train_number = f"{line_code}{random.randint(100, 999)}"
        
        # Add to schedule
        schedule.append({
            "time": time_str,
            "destination": destination,
            "destination_fr": STATION_FR.get(destination, destination),
            "line": line_code,
            "status": status,
            "platform": platform if status == "On time" else None,
            "delay_minutes": delay_minutes,
            "accessible": is_accessible,
            "train_number": train_number
        })
    
    # Sort by departure time
    schedule.sort(key=lambda x: x["time"])
    
    return schedule


def get_station_schedule(station_name):
    """
    Get the schedule for a specific station
    
    Args:
        station_name (str): Name of the station
        
    Returns:
        dict: Station data including schedule
    """
    # Validate station name
    if station_name not in STATIONS:
        station_name = STATIONS[0]  # Default to Union
    
    # Generate demo schedule
    train_schedule = generate_demo_schedule(station_name)
    
    # Prepare station data
    station_data = {
        "name": station_name,
        "name_fr": STATION_FR.get(station_name, station_name),
        "trains": train_schedule,
        "updated": datetime.now().strftime("%H:%M")
    }
    
    return station_data


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