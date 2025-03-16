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

    def generate_schedule(self, station, num_trains=48):
        """
        Generate a realistic train schedule for a given station based on GTFS data

        Args:
            station (str): Station name
            num_trains (int): Number of trains to generate (split between directions)

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

        from stop_scraper import stop_scraper

        # Time intervals for better distribution
        peak_interval = 10  # Minutes between trains during peak
        off_peak_interval = 20  # Minutes between trains during off-peak

        # Initialize schedule
        schedule = []

        # Generate trains for the number requested
        for i in range(num_trains):
            # Determine if peak hours (7-10am and 4-7pm)
            current_hour = (now + timedelta(minutes=i*10)).hour
            is_peak = (7 <= current_hour <= 10) or (16 <= current_hour <= 19)
            interval = peak_interval if is_peak else off_peak_interval

            # Generate departure time
            departure_time = now + timedelta(minutes=interval * i)

            # Generate trains in both directions
            line_code = random.choice(available_lines)
            # Get line stations and determine direction
            is_outbound = (i % 2 == 0)
            if is_outbound:
                if station == "Union Station":
                    destination = stop_scraper.get_stops_for_route(line_code)[-1]
                    stops = stop_scraper.get_upcoming_stops(station, destination, line_code)
                    stops_display = stop_scraper.format_stops_display(stops)
                else:
                    line_stations = stop_scraper.get_stops_for_route(line_code)
                    try:
                        if line_stations.index(station) >= len(line_stations) - 1:
                            continue  # Skip if at terminus
                        destination = line_stations[-1]
                        stops = stop_scraper.get_upcoming_stops(station, destination, line_code)
                        stops_display = stop_scraper.format_stops_display(stops)
                    except ValueError:
                        continue
            else:  # Inbound
                if station == "Union Station":
                    continue  # Skip inbound for Union
                else:
                    destination = "Union Station"
                    stops = stop_scraper.get_upcoming_stops(station, destination, line_code)
                    stops_display = stop_scraper.format_stops_display(stops)

            # Randomly assign train status based on weights
            status = random.choices(STATUS_OPTIONS, STATUS_WEIGHTS)[0]

            # Calculate delay if applicable
            delay_minutes = 0
            if status == "Delayed":
                delay_minutes = random.randint(5, 30)

            # Randomly assign platform
            platform = f"{random.randint(1, 12)}"

            # Generate train number and determine if express
            train_number = f"{line_code}{random.randint(100, 999)}"
            is_express = random.random() < 0.3  # 30% chance of being express

            # Get accessibility info
            if station_info:
                is_accessible = station_info.get('accessible', True)
            else:
                is_accessible = True

            # Determine if train is at platform
            at_platform = random.random() < 0.1  # 10% chance of being at platform
            if at_platform:
                status = "At Platform"

            # Calculate estimated arrival for upcoming trains
            if not at_platform and status == "On time":
                estimated = "On time"
            elif status == "Delayed":
                estimated = f"{delay_minutes} min delay"
            else:
                estimated = status

            # Clean destination name
            destination = destination.replace(" GO", "").replace(" Station", "")
            # Format stops for display with bullet points
            stops_display = " • ".join(stops) if stops else "Express Service"

            # Add to schedule with cleaned up display
            schedule.append({
                "departure_time": departure_time,
                "destination": destination + ('  EXPRESS' if is_express else ''),
                "destination_fr": destination + ('  EXPRESS' if is_express else ''),
                "status": status,
                "estimated": estimated,
                "platform": platform if status in ["On time", "At Platform"] else None,
                "route_code": line_code,
                "accessible": is_accessible,
                "train_number": train_number,
                "color": self.get_line_color(line_code),
                "is_express": is_express,
                "at_platform": at_platform,
                "stops": stops_display.replace('(BR)', '').replace('(LW)', '').replace('(LE)', '')
            })

        # Sort schedule:
        # 1. Trains at platform first
        # 2. Then by departure time
        schedule.sort(key=lambda x: (not x["at_platform"], x["departure_time"]))

        return schedule

# Create an instance for importing
scraper = GoScraper()