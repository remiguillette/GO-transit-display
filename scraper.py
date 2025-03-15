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
