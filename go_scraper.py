from datetime import datetime, timedelta
import random
import logging
from gtfs_parser import gtfs_data

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Status options
STATUS_OPTIONS = ["On time", "Delayed", "Cancelled"]
STATUS_WEIGHTS = [0.85, 0.10, 0.05]  # Probabilities for each status

class GoScraper:
    """Scraper for GO Transit schedules"""
    
    def __init__(self):
        # Make sure GTFS data is loaded
        if not gtfs_data.stations:
            gtfs_data.load_data()
    
    def get_line_color(self, line_code):
        """Get the official GO Transit color for a line code"""
        return gtfs_data.get_line_color(line_code)
    
    def get_available_stations(self):
        """Return the list of available stations from GTFS data"""
        return gtfs_data.get_station_names()
    
    def get_station_schedule(self, station_name):
        """
        Get the schedule for a specific station
        
        Args:
            station_name (str): Name of the station
            
        Returns:
            list: List of schedule dictionaries ready for display
        """
        # Ensure GTFS data is loaded
        if not gtfs_data.stations:
            gtfs_data.load_data()
        
        # Get available stations
        available_stations = self.get_available_stations()
        
        # Validate station name, default to Union if not found
        if station_name not in available_stations:
            if "Union Station" in available_stations:
                station_name = "Union Station"
            elif "Union" in available_stations:
                station_name = "Union"
            else:
                station_name = available_stations[0]
        
        # Generate schedule
        train_schedule = self.generate_schedule(station_name)
        
        return train_schedule
    
    def generate_schedule(self, station, num_trains=12):
        """
        Generate a realistic train schedule for a given station based on GTFS data
        
        Args:
            station (str): Station name
            num_trains (int): Number of trains to generate
            
        Returns:
            list: List of train schedule dictionaries
        """
        logger.debug(f"Generating schedule for {station}")
        
        # Initialize schedule
        schedule = []
        
        # Current time for reference
        now = datetime.now()
        
        # Identify station in GTFS data
        station_info = gtfs_data.get_station_by_name(station)
        
        # If station not found, default to Union
        if not station_info:
            logger.warning(f"Station '{station}' not found in GTFS data, defaulting to Union")
            for station_code, info in gtfs_data.stations.items():
                if info['name'] == 'Union Station':
                    station_info = info
                    break
        
        # Get available lines for this station
        available_lines = station_info.get('lines', []) if station_info else []
        
        # If no lines found, use default lines
        if not available_lines:
            available_lines = ['LW', 'LE', 'ST', 'RH', 'BR', 'KI', 'MI']
        
        # Time interval between trains (minutes)
        interval = 15
        
        # Generate schedule entries
        for i in range(num_trains):
            # Generate departure time 
            departure_time = now + timedelta(minutes=interval * i)
            
            # Select a random line for this train
            line_code = random.choice(available_lines)
            
            # Get appropriate destination based on line and station
            if station == "Union Station" or station == "Union":
                # Outbound from Union
                destinations = {
                    "LW": ["Hamilton GO Centre", "Aldershot GO", "West Harbour GO", "Niagara Falls GO"],
                    "LE": ["Oshawa GO"],
                    "ST": ["Lincolnville GO", "Mount Joy GO", "Unionville GO"],
                    "RH": ["Richmond Hill GO"],
                    "BR": ["Barrie GO", "Aurora GO", "Bradford GO"],
                    "KI": ["Kitchener GO", "Bramalea GO", "Mount Pleasant GO", "Georgetown GO"],
                    "MI": ["Milton GO"]
                }
                destination = random.choice(destinations.get(line_code, ["Oakville GO"]))
            else:
                # Inbound to Union
                destination = "Union Station"
            
            # Randomly assign train status based on weights
            status = random.choices(STATUS_OPTIONS, STATUS_WEIGHTS)[0]
            
            # Calculate delay if applicable
            delay_minutes = 0
            if status == "Delayed":
                delay_minutes = random.randint(5, 30)
            
            # Randomly assign platform
            platform = f"{random.randint(1, 12)}"
            
            # Generate train number
            train_number = f"{line_code}{random.randint(100, 999)}"
            
            # Get accessibility info
            if station_info:
                is_accessible = station_info.get('accessible', True)
            else:
                is_accessible = True
            
            # Add to schedule
            schedule.append({
                "departure_time": departure_time,
                "destination": destination,
                "destination_fr": destination,  # Default to English if French not available
                "status": status,
                "platform": platform if status == "On time" else None,
                "route_code": line_code,
                "accessible": is_accessible,
                "train_number": train_number,
                "color": self.get_line_color(line_code)
            })
        
        # Sort by departure time
        schedule.sort(key=lambda x: x["departure_time"])
        
        return schedule

# Create an instance for importing
scraper = GoScraper()