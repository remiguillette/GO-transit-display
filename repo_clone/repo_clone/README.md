# GO Transit Display Board

A Flask-based GO Transit display board application that shows real-time train departures with proper branding and accessibility features.

## Features

- Real-time train schedule display
- GO Transit branding and colors
- Bilingual support (English/French)
- Accessibility features
- Mobile-responsive design
- Station selection control panel

## Screenshots

![Display Board](https://via.placeholder.com/800x400?text=GO+Transit+Display+Board)
![Control Panel](https://via.placeholder.com/800x400?text=Control+Panel)

## Installation

Please refer to the [Installation Guide](INSTALLATION.md) for detailed setup instructions.

```bash
# Quick start with Flask development server
python main.py

# Or with Gunicorn (recommended for production)
gunicorn --bind 0.0.0.0:5000 --workers=4 main:app
```

## Usage

1. Navigate to the main page to view the display board
2. Use the control panel (`/control` endpoint) to select different stations
3. The board auto-refreshes every minute to show updated schedules

## Project Structure

The project follows a standard Flask structure with the following key files:

- `main.py` - Main Flask application entry point
- `scraper.py` - GO Transit schedule data handling and demo data generation
- `/templates` - HTML templates for the web interface
- `/static` - Static assets including CSS, fonts and SVG icons

For more details, see [Project Structure](attached_assets/PROJECT_STRUCTURE.md).

## Contributing

Contributions are welcome! Please read [Contributing Guidelines](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- GO Transit for branding inspiration
- Polaris font family for typography