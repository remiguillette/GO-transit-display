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
    """Scraper for GO Transit schedules with display protections"""

    def __init__(self):
        if not gtfs_data.stations:
            gtfs_data.load_data()

    def get_line_color(self, line_code):
        """Get the official GO Transit color for a line code"""
        return gtfs_data.get_line_color(line_code)

    def get_available_stations(self):
        """Return the list of available stations from GTFS data"""
        return gtfs_data.get_station_names()

    def get_station_schedule(self, station_name):
        """Get schedule for a station, ensuring stops column is protected"""
        logger.debug(f"Generating schedule for {station_name}")

        # Ensure GTFS data is loaded
        if not gtfs_data.stations:
            gtfs_data.load_data()

        # Get available stations
        available_stations = self.get_available_stations()

        # Validate station name
        if station_name not in available_stations:
            station_name = "Union Station" if "Union Station" in available_stations else available_stations[0]

        # Get station info
        station_info = gtfs_data.get_station_by_name(station_name)
        if not station_info:
            logger.warning(f"Station '{station_name}' not found")
            return []

        # Generate schedule
        train_schedule = []
        now = datetime.now()

        # Get available lines for station
        available_lines = station_info.get('lines', [])
        if not available_lines:
            available_lines = ['LW', 'LE', 'ST', 'RH', 'BR', 'KI', 'MI']

        # Time intervals
        peak_interval = 10  # Minutes between trains during peak
        off_peak_interval = 20  # Minutes between trains during off-peak

        # Generate schedule
        for i in range(48):  # 48 trains total
            # Determine peak hours
            current_hour = (now + timedelta(minutes=i*10)).hour
            is_peak = (7 <= current_hour <= 10) or (16 <= current_hour <= 19)
            interval = peak_interval if is_peak else off_peak_interval

            # Generate departure time 
            departure_time = now + timedelta(minutes=interval * i)

            # Generate train data
            line_code = random.choice(available_lines)
            is_outbound = (i % 2 == 0)

            # Set destination based on direction
            if is_outbound:
                if station_name == "Union Station":
                    terminals = gtfs_data.get_terminals(line_code)
                    destination = terminals[-1] if terminals else "Unknown"
                else:
                    terminals = gtfs_data.get_terminals(line_code)
                    destination = terminals[-1] if terminals else "Union Station"
            else:
                destination = "Union Station"

            # Clean destination name
            destination = destination.replace(" GO", "").replace(" Station", "")

            # Generate train details
            status = random.choices(STATUS_OPTIONS, STATUS_WEIGHTS)[0]
            delay_minutes = random.randint(5, 30) if status == "Delayed" else 0
            platform = f"{random.randint(1, 12)}"
            train_number = f"{line_code}{random.randint(100, 999)}"
            is_express = random.random() < 0.3
            at_platform = random.random() < 0.1

            # Status display
            if at_platform:
                status = "At Platform"
            estimated = "On time" if status == "On time" else (f"{delay_minutes} min delay" if status == "Delayed" else status)

            # Add schedule entry with empty stops column
            train_schedule.append({
                "departure_time": departure_time,
                "destination": destination + ('  EXPRESS' if is_express else ''),
                "destination_fr": destination + ('  EXPRESS' if is_express else ''),
                "status": status,
                "estimated": estimated,
                "platform": platform if status in ["On time", "At Platform"] else None,
                "route_code": line_code,
                "accessible": True,
                "train_number": train_number,
                "color": self.get_line_color(line_code),
                "is_express": is_express,
                "at_platform": at_platform,
                "stops": "" # Protected - stops not displayed by GO scraper
            })

        # Sort schedule by platform presence and time
        train_schedule.sort(key=lambda x: (not x["at_platform"], x["departure_time"]))

        return train_schedule

# Create an instance for importing
scraper = GoScraper()