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

    def generate_schedule(self, station_name):
        """
        Generate a schedule for a specific station using stop_scraper

        Args:
            station_name (str): Name of the station

        Returns:
            list: List of schedule dictionaries ready for display
        """
        try:
            from stop_scraper import stop_scraper
            schedule = stop_scraper.generate_schedule(station_name)
            if not schedule:
                logger.warning(f"No schedule generated for {station_name}")
                return []
            return schedule
        except Exception as e:
            logger.error(f"Error generating schedule: {str(e)}")
            return []

# Create an instance for importing
scraper = GoScraper()